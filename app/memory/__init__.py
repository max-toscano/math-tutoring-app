"""
memory/
Three-layer memory system for the ReAct tutoring agent.

- long_term.py  : Student profile, mastery scores, learning preferences (Supabase)
- session.py    : Current session state, problems attempted, streak (Supabase)
- short_term.py : In-memory message list for the current ReAct loop (no DB)
"""
