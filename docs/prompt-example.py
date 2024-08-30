def get_job_ratings(original_df, db_user, user_configs):
    jobs_df = original_df.copy()
    db_job_titles = [config['string_value'] for config in user_configs if config['key'] == 'job_titles']
    db_skill_words = [config['string_value'] for config in user_configs if config['key'] == 'skill_words']
    db_stop_words = [config['string_value'] for config in user_configs if config['key'] == 'stop_words']
    db_resume = db_user.get('resume')

    job_titles = db_job_titles or []
    skill_words = db_skill_words or []
    stop_words = db_stop_words or []

    resume = consolidate_text(db_resume)

    for index, row in jobs_df.iterrows():
        job_title = row.get('title', "N/A")
        job_description = row.get('description', "N/A")
        job_description = consolidate_text(job_description)

        full_message = f"<job_titles>{', '.join(job_titles)}</job_titles>\n" + \
                       f"<desired_words>{', '.join(skill_words)}</desired_words>\n" + \
                       f"<undesirable_words>{', '.join(stop_words)}</undesirable_words>\n" + \
                       f"<resume>{resume}</resume>\n" + \
                       f"<job_title>{job_title}</job_title>\n" + \
                       f"<job_description>{job_description}</job_description>\n" + \
                       """
                       Given the job titles (job_titles tag), desired words (desired_words tag), undesired words 
                       (undesirable_words tag), resume (resume tag), job title (job_title tag) and job description 
                       (job_description tag), make the following ratings:
                       
                       1) How the candidate would rate this job on a scale from 1 to 100 in terms of how well it 
                       matches their experience and the type of job they desire.
                       2) How the candidate would rate this job on a scale from 1 to 100 as a match for their 
                       experience level (they aren't underqualified or overqualified).
                       3) How a hiring manager for this job would rate the candidate on a scale from 1 to 100 on how 
                       well the candidate meets the skill requirements for this job.
                       4) How a hiring manager for this job would rate the candidate on a scale from 1 to 100 on how 
                       well the candidate meets the experience requirements for this job.
                       5) Consider the results from steps 1 through 5 then give a final assessment from 1 to 100,
                       where 1 is very little chance of this being a good match for the candidate and hiring manager, 
                       and 100 being a perfect match where the candidate will have a great chance to succeed in 
                       this role.
                       
                       For experience level, look for cues in the jobs description that list years of experience, 
                       then compare that to the level of experience you believe the candidate to have (make an 
                       assessment based on year in directly applicable fields of work).
                       
                       Start your answer immediately with a bulleted list as shown in the example below. Always include 
                       the left side prefix from the template below in your answer (including for the explanation). 
                       Address the candidate directly, closely following the template set in the example. NN should be 
                       replaced in the template with a 2 digit number each time.
                       """
        full_message = consolidate_text(full_message)
        full_message += \
            """
            - Candidate desire match: NN
            - Candidate experience match: NN
            - Hiring manager skill match: NN
            - Hiring manager experience match: NN
            - Final overall match assessment: NN
            - Explanation of ratings: 
            You may <like, be lukewarm on, or dislike> this job because of the following reasons: <reasons in one sentence>. The hiring manager may think you would be a <good, reasonable, or bad> fit for this job because of <reasons, in one sentence>. Overall, I think <your overall thoughts about the match between the user and the job in one sentence>.
            """

        ratings = query_llm(llm="openai",
                            model_name="gpt-4o-mini",
                            system="You are a helpful no-nonsense assistant. You listen to directions carefully and follow them to the letter.",
                            messages=[{"role": "user", "content": full_message}])

        if ratings is None:
            print("LLM failed to generate ratings.")
            continue

        print(f"Ratings for job {index}: {ratings}")
		
		
def query_llm(llm, model_name, system, messages=[]):
    max_retries = 3
    wait_time = 3

    for attempt in range(max_retries):
        try:
            if llm == "openai":
                messages.insert(0, {"role": "system", "content": system})
                client = OpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY"),
                )
                completion = client.chat.completions.create(
                    messages=messages,
                    max_tokens=256,
                    model=model_name,
                    temperature=1.0
                )
                return completion.choices[0].message.content
            elif llm == "anthropic":
                anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
                client = anthropic.Anthropic(api_key=anthropic_api_key)
                message = client.messages.create(
                    model=model_name,
                    max_tokens=256,
                    temperature=1.0,
                    system=system,
                    messages=messages
                )
                return message.content[0].text
            elif llm == "gemini":
                safe = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE",
                    }
                ]

                gemini.configure(api_key=os.environ.get("GEMINI_API_KEY"))
                model = gemini.GenerativeModel(model_name=model_name, safety_settings=safe)  # 'gemini-1.5-flash'
                response = model.generate_content(system + " " + " ".join([msg["content"] for msg in messages]))
                return response.text
            else:
                return None

        except Exception as e:
            print(
                f"An unexpected error occurred: {e}. Attempt {attempt + 1} of {max_retries}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            wait_time *= 2  # Exponential backoff
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts.")
                return None

    return None