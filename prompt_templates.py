# prompt_templates.py

PODCAST_INTERVIEW_PROMPT = """
You are an expert podcast scriptwriter specializing in crafting engaging and insightful interview questions.

I am hosting a podcast episode featuring {guest_name}, who is an expert in {expertise}. I need {num_questions} high-quality interview questions that match a {tone} tone.

For each question:
1. Ensure it is thought-provoking and encourages deep discussion.
2. Keep it relevant to the guest’s expertise and industry trends.
3. Make it engaging for both the guest and the audience.
4. Avoid generic or overused questions—aim for fresh and unique insights.

The questions should flow naturally in a structured interview format. If necessary, include follow-up question suggestions to dive deeper into key topics.

Format the output as a numbered list of questions without additional text.
"""
