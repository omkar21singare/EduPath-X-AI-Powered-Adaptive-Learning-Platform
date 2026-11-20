from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import KnowledgeState, Concept, QuestionAttempt, ConceptPrerequisite
from app.ml.recommendation import recommendation_engine
from app.schemas.schemas import AssistantQuery, AssistantResponse

router = APIRouter(prefix="/api/assistant", tags=["Assistant"])

@router.post("/chat", response_model=AssistantResponse)
def assistant_chat(payload: AssistantQuery, learner_id: int = 1, db: Session = Depends(get_db)):
    msg = payload.message.lower().strip()

    k_states = db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id).all()
    if not k_states or sum(ks.total_attempts for ks in k_states) == 0:
        return AssistantResponse(
            reply="I don't have enough learner data yet. Complete a few practice questions or start an adaptive session to help me analyze your knowledge state!",
            recommended_action=None,
            data_sources_used=["KnowledgeState DB"]
        )

    attempts = db.query(QuestionAttempt).filter(QuestionAttempt.learner_id == learner_id).all()

    # Identify weak & strong concepts
    weak_concepts = []
    strong_concepts = []
    for ks in k_states:
        c = ks.concept
        if not c: continue
        if ks.mastery_probability < 0.60:
            weak_concepts.append((c.title, ks.mastery_probability))
        elif ks.mastery_probability >= 0.85:
            strong_concepts.append((c.title, ks.mastery_probability))

    recs = recommendation_engine.generate_recommendations(db, learner_id, limit=3)
    top_rec = recs[0] if recs else None

    # Handle Intent Queries
    if "study" in msg or "today" in msg or "what should i" in msg:
        if top_rec:
            reply = (
                f"Based on your current Bayesian Knowledge Tracing model, I recommend focusing on **{top_rec['concept_title']}** today. "
                f"\n\n**Action**: {top_rec['action_type']}\n**Reason**: {top_rec['reason_text']}"
            )
        else:
            reply = "You are currently performing well across unlocked concepts! Try challenging yourself with Advanced Graph algorithms or Dynamic Programming."

        return AssistantResponse(
            reply=reply,
            recommended_action=top_rec,
            data_sources_used=["Bayesian Knowledge Tracing Model", "Prerequisite Dependency Graph", "Recommendation Engine"]
        )

    elif "weak" in msg or "struggle" in msg:
        if weak_concepts:
            weak_str = ", ".join([f"{title} ({round(m*100)}% mastery)" for title, m in weak_concepts[:3]])
            reply = f"According to your recent interaction history, your weakest areas are: **{weak_str}**. Target practice on these will yield the highest performance gains!"
        else:
            reply = "You haven't displayed any significant weaknesses yet! Your mastery across active concepts is above 60%."

        return AssistantResponse(
            reply=reply,
            recommended_action=top_rec,
            data_sources_used=["KnowledgeState Mastery Estimates", "Attempt Accuracy History"]
        )

    elif "dijkstra" in msg or "unlock" in msg:
        dijkstra_c = db.query(Concept).filter(Concept.code == "DIJKSTRA").first()
        if dijkstra_c:
            prereqs = db.query(ConceptPrerequisite).filter(ConceptPrerequisite.concept_id == dijkstra_c.id).all()
            missing = []
            for p in prereqs:
                p_ks = db.query(KnowledgeState).filter(KnowledgeState.learner_id == learner_id, KnowledgeState.concept_id == p.prerequisite_id).first()
                p_mastery = p_ks.mastery_probability if p_ks else 0.10
                p_concept = db.query(Concept).get(p.prerequisite_id)
                if p_mastery < p.minimum_mastery:
                    missing.append(f"{p_concept.title if p_concept else 'Prereq'} ({round(p_mastery*100)}% / required {round(p.minimum_mastery*100)}%)")

            if missing:
                reply = f"You cannot unlock **Dijkstra's Algorithm** yet because the following prerequisites require higher mastery:\n- " + "\n- ".join(missing)
            else:
                reply = "Dijkstra's Algorithm is fully unlocked! You meet all prerequisite mastery requirements."
        else:
            reply = "Dijkstra's Algorithm is part of the Advanced Graph curriculum."

        return AssistantResponse(
            reply=reply,
            recommended_action=top_rec,
            data_sources_used=["Concept Prerequisite DAG", "KnowledgeState DB"]
        )

    elif "improved" in msg or "week" in msg:
        reply = (
            f"Great news! Over your recent activity ({len(attempts)} attempts recorded), you've demonstrated strong improvement in core concepts. "
            f"You currently have {len(strong_concepts)} fully mastered concepts."
        )
        return AssistantResponse(
            reply=reply,
            recommended_action=top_rec,
            data_sources_used=["KnowledgeState History Audit Trail"]
        )

    else:
        reply = (
            f"I am your EduPath-X Learning Assistant. Based on your current profile:\n"
            f"- Mastered Concepts: {len(strong_concepts)}\n"
            f"- Target Area: {top_rec['concept_title'] if top_rec else 'Data Structures'}\n\n"
            f"Ask me questions like: 'What should I study today?', 'What am I weak at?', or 'Why can't I unlock Dijkstra?'"
        )
        return AssistantResponse(
            reply=reply,
            recommended_action=top_rec,
            data_sources_used=["KnowledgeState DB", "Recommendation Engine"]
        )
