decompose_prompt = """
Your task is to decompose the text into atomic claims.
The answer should be a JSON with a single key "claims", with the value of a list of strings, where each string should be a context-independent claim, representing one fact.
Note that:
1. Each claim should be concise (less than 15 words) and self-contained.
2. Avoid vague references like 'he', 'she', 'it', 'this', 'the company', 'the man' and using complete names.
3. Generate at least one claim for each single sentence in the texts.

For example,
Text: Mary is a five-year old girl, she likes playing piano and she doesn't like cookies.
Output:
{{"claims": ["Mary is a five-year old girl.", "Mary likes playing piano.", "Mary doesn't like cookies."]}}

Text: {doc}
Output:
"""

checkworthy_prompt = """
Your task is to evaluate each provided statement to determine if it presents information whose factuality can be objectively verified by humans, irrespective of the statement's current accuracy. Consider the following guidelines:
1. Opinions versus Facts: Distinguish between opinions, which are subjective and not verifiable, and statements that assert factual information, even if broad or general. Focus on whether there's a factual claim that can be investigated.
2. Clarity and Specificity: Statements must have clear and specific references to be verifiable (e.g., "he is a professor" is not verifiable without knowing who "he" is).
3. Presence of Factual Information: Consider a statement verifiable if it includes factual elements that can be checked against evidence or reliable sources, even if the overall statement might be broad or incorrect.
Your response should be in JSON format, with each statement as a key and either "Yes" or "No" as the value, along with a brief rationale for your decision.

For example, given these statements:
1. Gary Smith is a distinguished professor of economics.
2. He is a professor at MBZUAI.
3. Obama is the president of the UK.

The expected output is:
{{
    "Gary Smith is a distinguished professor of economics.": "Yes (The statement contains verifiable factual information about Gary Smith's professional title and field.)",
    "He is a professor at MBZUAI.": "No (The statement cannot be verified due to the lack of clear reference to who 'he' is.)",
    "Obama is the president of the UK.": "Yes (This statement contain verifiable information regarding the political leadership of a country.)"
}}

For these statements:
{texts}

The output should be:
"""

qgen_prompt = """Given a claim, your task is to create minimum number of questions need to be check to verify the correctness of the claim. Output in JSON format with a single key "Questions", the value is a list of questions. For example:

Claim: Your nose switches back and forth between nostrils. When you sleep, you switch about every 45 minutes. This is to prevent a buildup of mucus. It’s called the nasal cycle.
Output: {{"Questions": ["Does your nose switch between nostrils?", "How often does your nostrils switch?", "Why does your nostril switch?", "What is nasal cycle?"]}}

Claim: The Stanford Prison Experiment was conducted in the basement of Encina Hall, Stanford’s psychology building.
Output:
{{"Question":["Where was Stanford Prison Experiment was conducted?"]}}

Claim: The Havel-Hakimi algorithm is an algorithm for converting the adjacency matrix of a graph into its adjacency list. It is named after Vaclav Havel and Samih Hakimi.
Output:
{{"Questions":["What does Havel-Hakimi algorithm do?", "Who are Havel-Hakimi algorithm named after?"]}}

Claim: Social work is a profession that is based in the philosophical tradition of humanism. It is an intellectual discipline that has its roots in the 1800s.
Output:
{{"Questions":["What philosophical tradition is social work based on?", "What year does social work have its root in?"]}}

Claim: {claim}
Output:
"""

verify_prompt = """
Your task is to evaluate the accuracy of a provided statement using the accompanying evidence. Carefully review the evidence, noting that it may vary in detail and sometimes present conflicting information. Your judgment should be informed by this evidence, taking into account its relevance and reliability.

Keep in mind that a lack of detail in the evidence does not necessarily indicate that the statement is inaccurate. When assessing the statement's factuality, distinguish between errors and areas where the evidence supports the statement.

Please structure your response in JSON format, including the following four keys:
- "reasoning": explain the thought process behind your judgment.
- "error": none if the text is factual; otherwise, identify any specific inaccuracies in the statement.
- "correction": none if the text is factual; otherwise, provide corrections to any identified inaccuracies, using the evidence to support your corrections.
- "factuality": true if the given text is factual, false otherwise, indicating whether the statement is factual, or non-factual based on the evidence.

For example:
Input:
[text]: MBZUAI is located in Abu Dhabi, United Arab Emirates.
[evidence]: Where is MBZUAI located?\nAnswer: Masdar City - Abu Dhabi - United Arab Emirates

Output:
{{
    "reasoning": "The evidence confirms that MBZUAI is located in Masdar City, Abu Dhabi, United Arab Emirates, so the statement is factually correct",
    "error": none,
    "correction": none,
    "factuality": true
}}


Input:
[text]: Copper reacts with ferrous sulfate (FeSO4).
[evidence]: Copper is less reactive metal. It has positive value of standard reduction potential. Metal with high standard reduction potential can not displace other metal with low standard reduction potential values. Hence copper can not displace iron from ferrous sulphate solution. So no change will take place.

Output:
{{
    "reasoning": "The evidence provided confirms that copper cannot displace iron from ferrous sulphate solution, and no change will take place.",
    "error": "Copper does not react with ferrous sulfate as stated in the text.",
    "correction": "Copper does not react with ferrous sulfate as it cannot displace iron from ferrous sulfate solution.",
    "factuality": false
}}


Input
[text]: {claim}
[evidences]: {evidence}

Output:
"""


class ChatGPTPrompt:
    decompose_prompt = decompose_prompt
    checkworthy_prompt = checkworthy_prompt
    qgen_prompt = qgen_prompt
    verify_prompt = verify_prompt
