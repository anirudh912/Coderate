from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

def get_code_review(code: str, analysis_results: str) -> str:
    try:
        # init model
        model_id = "codellama/CodeLlama-7b-hf"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        # make pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.4,
            pad_token_id=tokenizer.eos_token_id
        )

        # LangChain pipeline
        llm = HuggingFacePipeline(pipeline=pipe)

        # prompt template
        prompt = f"""
        As a senior software engineer, review this code and static analysis findings.
        Provide clear, actionable suggestions using markdown formatting.

        Code:
        {code}

        Static Analysis Results:
        {analysis_results}

        Requirements:
        1. Explain each issue clearly
        2. Provide corrected code snippets
        3. Highlight best practices
        4. Keep suggestions practical

        Review:
        """

        return llm.invoke(prompt)
    except Exception as e:
        return f"AI review failed: {str(e)}"
