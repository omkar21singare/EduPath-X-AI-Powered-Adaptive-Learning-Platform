import os
import json
import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import KnowledgeState, Concept, QuestionAttempt, ConceptPrerequisite, LearningMaterial, Question
from app.ml.recommendation import recommendation_engine
from app.schemas.schemas import AssistantQuery, AssistantResponse
from app.core.auth import resolve_learner_id, get_current_user_optional
from app.models.models import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/assistant", tags=["Assistant"])

def call_gemini_api(prompt: str, api_key: str) -> Optional[str]:
    """Call Google Gemini API via httpx if api key is provided."""
    try:
        import httpx
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 800}
        }
        with httpx.Client(timeout=8.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        logger.warning(f"Gemini API request failed or offline: {e}")
    return None

def build_smart_pedagogical_response(
    query: str,
    learner_id: int,
    k_states: List[KnowledgeState],
    attempts: List[QuestionAttempt],
    recommendations: List[Dict[str, Any]],
    materials: List[LearningMaterial],
    db: Session
) -> str:
    """
    Intelligent context engine that synthesizes mastery, error patterns,
    active learning trajectories, and textbook excerpts.
    """
    weak = [ks for ks in k_states if ks.mastery_probability < 0.60]
    mastered = [ks for ks in k_states if ks.mastery_probability >= 0.85]
    in_progress = [ks for ks in k_states if 0.60 <= ks.mastery_probability < 0.85]

    total_attempts = len(attempts)
    recent_wrong = [a for a in attempts if not a.is_correct][-5:]
    recent_wrong_concepts = set()
    for rw in recent_wrong:
        q = db.query(Question).filter(Question.id == rw.question_id).first()
        if q and q.concept:
            recent_wrong_concepts.add(q.concept.title)

    top_rec = recommendations[0] if recommendations else None

    # Synthesize intelligent guidance
    response_sections = []

    # 1. State synthesis
    response_sections.append(
        f"### Knowledge State Synthesis\n"
        f"- **Curriculum Mastery**: {len(mastered)} mastered, {len(in_progress)} in progress, and {len(weak)} areas needing consolidation.\n"
        f"- **Engagement Volume**: {total_attempts} total problem evaluations analyzed."
    )

    # 2. Targeted Diagnostic & Pedagogical Advice
    if top_rec:
        rec_title = top_rec.get("concept_title", "Data Structures")
        rec_action = top_rec.get("action_type", "PRACTICE")
        rec_reason = top_rec.get("reason_text", "To solidify foundations.")
        response_sections.append(
            f"### Recommended Priority Action\n"
            f"Your current optimal learning frontier points to **{rec_title}** ({rec_action}).\n"
            f"> *Pedagogical Rationale:* {rec_reason}"
        )

    # 3. Weak Concept & Diagnostic Analysis
    if weak or recent_wrong_concepts:
        weak_details = ", ".join([f"**{w.concept.title}** ({round(w.mastery_probability * 100)}%)" for w in weak[:3] if w.concept])
        err_note = f" Recent misconceptions were detected in: {', '.join(recent_wrong_concepts)}." if recent_wrong_concepts else ""
        response_sections.append(
            f"### Targeted Remediation\n"
            f"Prioritize reinforcement on {weak_details or 'recently attempted modules'}.{err_note} "
            f"Focusing on foundational invariants before tackling complex multi-step variations will accelerate mastery stability."
        )

    # 4. Relevant Concept Material Excerpts if available
    matched_materials = []
    query_tokens = query.lower().split()
    for mat in materials:
        if any(tok in mat.title.lower() or (mat.concept and tok in mat.concept.title.lower()) for tok in query_tokens):
            matched_materials.append(mat)

    if matched_materials:
        mat = matched_materials[0]
        c_title = mat.concept.title if mat.concept else mat.title
        response_sections.append(
            f"### Concept Reference: {c_title}\n"
            f"{mat.summary or mat.content[:350]}..."
        )

    response_sections.append(
        f"\n*Generated using live BKT mastery trace, prerequisite graph topological ordering, and Bayesian parameter calibration.*"
    )

    return "\n\n".join(response_sections)

@router.post("/chat", response_model=AssistantResponse)
def assistant_chat(
    payload: AssistantQuery,
    learner_id: Optional[int] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    resolved_id = resolve_learner_id(learner_id, current_user, db)
    query_text = payload.message.strip()

    k_states = db.query(KnowledgeState).filter(KnowledgeState.learner_id == resolved_id).all()
    attempts = db.query(QuestionAttempt).filter(QuestionAttempt.learner_id == resolved_id).all()
    recs = recommendation_engine.generate_recommendations(db, resolved_id, limit=3)
    top_rec = recs[0] if recs else None
    materials = db.query(LearningMaterial).all()

    # If API key configured, invoke Gemini LLM with context
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        context_data = {
            "learner_id": resolved_id,
            "mastery": [{"concept": ks.concept.title if ks.concept else "", "prob": ks.mastery_probability} for ks in k_states],
            "total_attempts": len(attempts),
            "top_recommendation": top_rec
        }
        prompt = (
            f"You are the EduPath-X pedagogical AI tutor. The learner has asked: '{query_text}'.\n"
            f"Current Learner Adaptive Analytics:\n{json.dumps(context_data, indent=2)}\n\n"
            f"Provide a helpful, precise, supportive response analyzing their knowledge state and next steps."
        )
        gemini_reply = call_gemini_api(prompt, gemini_key)
        if gemini_reply:
            return AssistantResponse(
                reply=gemini_reply,
                recommended_action=top_rec,
                data_sources_used=["Google Gemini 1.5 Flash", "BKT Engine", "Curriculum Knowledge Graph"]
            )

    # Intelligent Context-Driven Synthesizer Fallback
    smart_reply = build_smart_pedagogical_response(
        query=query_text,
        learner_id=resolved_id,
        k_states=k_states,
        attempts=attempts,
        recommendations=recs,
        materials=materials,
        db=db
    )

    return AssistantResponse(
        reply=smart_reply,
        recommended_action=top_rec,
        data_sources_used=["Adaptive Context Engine", "Live BKT State DB", "Prerequisite Knowledge Graph", "OpenCourseWare Excerpts"]
    )
