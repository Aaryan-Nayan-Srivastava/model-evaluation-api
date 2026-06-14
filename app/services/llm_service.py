from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser
from app.schemas.response_schema import LLMEvaluationOutput
from langchain_core.exceptions import OutputParserException
import os
load_dotenv()
def get_llm()->ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")
    if api_key is None:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    
    return ChatGroq(model=model_name, temperature=0.2, api_key=api_key)



def get_output_parser() -> PydanticOutputParser:

    return PydanticOutputParser(pydantic_object=LLMEvaluationOutput)


def get_format_instructions() -> str:


    parser = get_output_parser()

    return parser.get_format_instructions()


async def generate_structured_llm_evaluation(prompt: str) -> LLMEvaluationOutput:
    """
    Send the prompt to Groq and parse the LLM output into LLMEvaluationOutput.

    This function is async because llm.ainvoke() performs a network call.
    """

    llm = get_llm()
    parser = get_output_parser()

    response = await llm.ainvoke(prompt)
    raw_output = response.content

    try:
        parsed_output = parser.parse(raw_output)
    except OutputParserException as exc:
        raise ValueError(
            "LLM returned output that could not be parsed into the required structure."
        ) from exc

    return parsed_output




