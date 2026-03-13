"""
response_patterns.py
Defines tutoring phrasing patterns for building natural, consistent tutor responses.
Each group targets a different moment in the tutoring interaction.
"""

# Opening lines to start a tutoring response.
openers: list[str] = [
    "Great question! Let's work through this together.",
    "Let's break this down step by step.",
    "Good try! Let me help you think through it.",
]

# Questions that nudge the student toward the answer without giving it away.
guided_questions: list[str] = [
    "What do you think the first step should be?",
    "What operation would you apply here?",
    "Does that result look reasonable to you?",
]

# Phrases used to transition between steps in a solution.
step_transitions: list[str] = [
    "Now that we have that, let's move to the next step.",
    "Good — with that in place, we can now look at...",
    "Here's where it gets interesting. Next, we...",
]

# Phrases used when the AI notices or corrects a common mistake.
mistake_corrections: list[str] = [
    "Not quite — let's look at that part again.",
    "Almost! There's a small error here. Can you spot it?",
    "This is a common slip. Remember to watch out for...",
]

# Phrases used to check whether the student understood before moving on.
learning_checkpoints: list[str] = [
    "Does that make sense so far?",
    "Before we continue, can you tell me why we did that step?",
    "Try repeating that back in your own words.",
]

# Closing lines to wrap up a tutoring response.
closers: list[str] = [
    "Does that make sense? Try the next one on your own!",
    "You've got it — keep practicing!",
    "Great work. Let me know if you want another example.",
]
