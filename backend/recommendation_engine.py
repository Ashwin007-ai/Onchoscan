import os

from groq import Groq


GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


CLASS_GUIDANCE = {
    "brain": {
        "glioma": {
            "specialist": "neuro-oncologist and neurosurgeon",
            "context": (
                "Emphasize contrast-enhanced MRI review, neurologic assessment, symptom progression, "
                "and urgent specialist planning if deficits, seizures, or raised intracranial pressure symptoms exist."
            ),
        },
        "meningioma": {
            "specialist": "neuro-oncologist and neurosurgeon",
            "context": (
                "Emphasize correlation with lesion size, mass effect, edema, headache or focal deficit burden, "
                "and whether interval imaging versus neurosurgical evaluation is appropriate."
            ),
        },
        "pituitary": {
            "specialist": "neuro-oncologist, neurosurgeon, and endocrinologist",
            "context": (
                "Emphasize visual symptoms, endocrine review, pituitary hormone testing, and timely specialist follow-up "
                "if headache, vision change, or hormonal symptoms are present."
            ),
        },
        "notumor": {
            "specialist": "neurologist or radiologist if symptoms persist",
            "context": (
                "Emphasize that a no-tumor pattern still requires clinical correlation if seizures, progressive headache, "
                "focal neurologic findings, or prior abnormal imaging remain concerning."
            ),
        },
    },
    "skin": {
        "benign": {
            "specialist": "dermatologist",
            "context": (
                "Emphasize lesion monitoring, dermoscopic review if clinically suspicious, and watching for asymmetry, "
                "border irregularity, color change, bleeding, itching, or rapid growth."
            ),
        },
        "malignant": {
            "specialist": "dermatologist and dermatologic oncologist",
            "context": (
                "Emphasize urgent dermatology review, dermoscopy, possible biopsy planning, documentation with lesion photography, "
                "and avoiding delay if the lesion is changing, bleeding, ulcerating, or darkening."
            ),
        },
    },
}


def _format_probabilities(probabilities: dict) -> str:
    lines = []
    for cls, pct in sorted(probabilities.items(), key=lambda x: -x[1]):
        lines.append(f"- {cls.title()}: {pct:.1f}%")
    return "\n".join(lines)


def _confidence_description(confidence: float) -> str:
    if confidence >= 88:
        return "very high confidence"
    if confidence >= 72:
        return "high confidence"
    if confidence >= 55:
        return "moderate confidence"
    return "low confidence"


def _check_differential(probabilities: dict) -> str:
    sorted_probs = sorted(probabilities.items(), key=lambda x: -x[1])
    if len(sorted_probs) < 2:
        return "No strong differential warning from class competition."

    top_cls, top_prob = sorted_probs[0]
    second_cls, second_prob = sorted_probs[1]
    gap = top_prob - second_prob

    if gap < 20.0:
        return (
            f"Differential diagnosis alert: {second_cls.title()} is the second-closest class at "
            f"{second_prob:.1f}% and only {gap:.1f}% below {top_cls.title()}."
        )

    return "Class separation is reasonably clear; no close second-class competitor."


def _get_guidance(cancer_type: str, prediction: str) -> dict:
    prediction_key = (prediction or "").lower()
    default_specialist = (
        "neuro-oncologist and neurosurgeon"
        if cancer_type == "brain"
        else "dermatologist and dermatologic oncologist"
    )
    guidance = CLASS_GUIDANCE.get(cancer_type, {}).get(prediction_key, {})
    return {
        "specialist": guidance.get("specialist", default_specialist),
        "context": guidance.get(
            "context",
            "Provide specific next-step precautions, follow-up planning, and symptom-based escalation advice.",
        ),
    }


def _build_prompt(
    cancer_type: str,
    prediction: str,
    confidence: float,
    risk_level: str,
    risk_score: int,
    probabilities: dict,
    gradcam_region: str,
    image_profile: dict,
    attention_profile: dict,
) -> str:
    guidance = _get_guidance(cancer_type, prediction)
    gradcam_text = (
        f"Grad-CAM suggests attention over: {gradcam_region}."
        if gradcam_region
        else "Grad-CAM region label is not available."
    )

    return f"""
You are a responsible clinical decision-support assistant for an AI cancer screening platform.
Your output must be more useful than a generic warning and must stay specific to the predicted cancer type.
The same cancer type may appear across multiple images, so you must vary the wording and focus based on the image-specific descriptors below.

Write a recommendation in EXACTLY 4 bullet points.
Each bullet must begin with "- ".
Each bullet must be one concise, clinically useful, action-oriented sentence.

The 4 bullets must cover:
1. What the AI pattern suggests in plain clinical language for this exact predicted class
2. Immediate next evaluation step to consider, with confidence percentage or risk score when useful
3. Monitoring, symptom escalation, or supportive measure relevant to this cancer type
4. Specialist follow-up and a reminder that this is AI-assisted screening, not a diagnosis

Strict rules:
- Do not write a paragraph
- Do not say "the patient has cancer"
- Say "the AI model suggests" or "the AI analysis indicates"
- Adjust urgency to the stated risk level
- If the second class is close, mention differential diagnosis briefly
- Be specific to {prediction.title()} rather than generic cancer advice
- Include concrete measures like imaging review, biopsy consideration, endocrine review, neurologic review, or lesion-change monitoring only when appropriate to this cancer type
- Avoid overclaiming and avoid treatment instructions beyond appropriate evaluation/follow-up
- Include the confidence percentage in at least 1 bullet
- Include the risk score in at least 1 bullet
- You may mention the most relevant percentages, but avoid turning every bullet into raw numbers
- At least 2 bullets must explicitly reflect the image-specific descriptors so outputs differ across scans
- Mention whether the attention pattern is focal, regional, or diffuse when clinically relevant
- If the image profile is dark, bright, soft-contrast, high-contrast, warm-toned, cool-toned, or neutral-toned, let that influence wording about review quality or correlation
- Do not use identical phrasing between scans when descriptors differ

Case details:
- Cancer type: {cancer_type.upper()}
- Predicted class: {prediction.title()}
- Confidence band: {_confidence_description(confidence)}
- Risk level: {risk_level}
- Risk score: {risk_score}/100
- Specialist to mention: {guidance['specialist']}
- Class-specific context: {guidance['context']}
- {gradcam_text}
- Image profile: brightness={image_profile['brightness_label']} ({image_profile['brightness']}), contrast={image_profile['contrast_label']} ({image_profile['contrast']}), tone={image_profile['color_label']}
- Attention profile: {attention_profile['focus_label']} attention, strong-activation area={attention_profile['focus_percent']}%, dominant zone={attention_profile['attention_zone']}
- Probability distribution:
{_format_probabilities(probabilities)}
- {_check_differential(probabilities)}

Return only the 4 bullet points.
""".strip()


def _fallback_recommendation(
    cancer_type: str,
    prediction: str,
    confidence: float,
    risk_level: str,
    risk_score: int,
    image_profile: dict | None = None,
    attention_profile: dict | None = None,
) -> str:
    guidance = _get_guidance(cancer_type, prediction)
    image_profile = image_profile or {}
    attention_profile = attention_profile or {}
    urgency = {
        "High Risk": "Arrange prompt specialist review without delay.",
        "Medium Risk": "Plan timely specialist review and correlate with symptoms and prior studies.",
        "Low Risk": "Use routine follow-up timing unless symptoms or imaging concerns increase.",
    }.get(risk_level, "Correlate with clinical findings and arrange appropriate follow-up.")

    image_note = (
        f"The uploaded image appears {image_profile.get('brightness_label', 'variable')}, "
        f"{image_profile.get('contrast_label', 'variable')}, and {image_profile.get('color_label', 'variable')}, "
        f"so interpretation should be correlated with image quality and the original study."
    )
    attention_note = (
        f"Grad-CAM shows a {attention_profile.get('focus_label', 'variable')} attention pattern centered in the "
        f"{attention_profile.get('attention_zone', 'variable')} region, which can help prioritize what to review first."
    )

    return "\n".join([
        f"- The AI model suggests image features most consistent with {prediction.title()}, with confidence {confidence:.1f}%, and this should be interpreted together with the full clinical picture.",
        f"- {urgency} Current risk score is {risk_score}/100, which should guide how quickly the case is reviewed.",
        f"- {image_note}",
        f"- {attention_note} Focus of follow-up: {guidance['context']} Consult {guidance['specialist']}; this is an AI-assisted screening output and not a confirmed diagnosis.",
    ])


def generate_recommendation(
    cancer_type: str,
    prediction: str,
    confidence: float,
    risk_level: str,
    risk_score: int,
    probabilities: dict,
    gradcam_region: str = "",
    image_profile: dict | None = None,
    attention_profile: dict | None = None,
) -> str:
    image_profile = image_profile or {
        "brightness": 0.0,
        "contrast": 0.0,
        "brightness_label": "unknown",
        "contrast_label": "unknown",
        "color_label": "unknown",
    }
    attention_profile = attention_profile or {
        "focus_label": "unknown",
        "focus_percent": 0.0,
        "attention_zone": "unknown",
    }
    prompt = _build_prompt(
        cancer_type,
        prediction,
        confidence,
        risk_level,
        risk_score,
        probabilities,
        gradcam_region,
        image_profile,
        attention_profile,
    )

    if not client:
        return _fallback_recommendation(
            cancer_type,
            prediction,
            confidence,
            risk_level,
            risk_score,
            image_profile,
            attention_profile,
        )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful clinical AI assistant. "
                        "You produce short, point-wise, cancer-specific recommendations from model outputs only. "
                        "You never diagnose, never overclaim, and always recommend appropriate specialist follow-up."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=260,
            temperature=0.2,
            top_p=0.9,
        )

        recommendation = (response.choices[0].message.content or "").strip()
        lines = [line.strip() for line in recommendation.splitlines() if line.strip()]
        bullet_lines = []

        for line in lines:
            cleaned = line.lstrip("0123456789.) ").strip()
            if not cleaned.startswith("- "):
                cleaned = "- " + cleaned.lstrip("-* ").strip()
            bullet_lines.append(cleaned)

        if not bullet_lines:
            raise ValueError("Empty recommendation response")

        return "\n".join(bullet_lines[:4])

    except Exception as e:
        print(f"[RecommendationEngine] Groq unavailable: {e}")
        return _fallback_recommendation(
            cancer_type,
            prediction,
            confidence,
            risk_level,
            risk_score,
            image_profile,
            attention_profile,
        )
