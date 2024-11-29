import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser

ontolgy_path = "ontology/dprod-anon-limited-v1.ttl"

if __name__ == "__main__":
    print("Hello OntoChat!")
    # print(os.environ.get("OPENAI_API_KEY"))

    with open(ontolgy_path, 'r', encoding='utf-8') as file:
        ontology = file.read()

    text_prompt_template = """
        Given that the following ontology {ontology} is my companie's data products ontology, I want to know:
         1- which types of data products my company offers;
         2- a sparql query to answer the same question.
        """

    summary_prompt_template = PromptTemplate(
        input_variables="ontology", template=text_prompt_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"ontology": ontology})

    print(res)
