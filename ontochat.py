import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain_community.graphs import OntotextGraphDBGraph
from langchain.chains import OntotextGraphDBQAChain

from dotenv import load_dotenv

load_dotenv()

ontolgy_path = "ontology/dprod-anon-limited-v1.ttl"

if __name__ == "__main__":
    print("Hello OntoChat!")

    # with open(ontolgy_path, 'r', encoding='utf-8') as file:
    #     ontology = file.read()

    
    #llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    #llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    #llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    
    graph = OntotextGraphDBGraph(
        query_endpoint="http://localhost:7200/repositories/mysandbox",
        local_file="ontology/dprod-anon-limited-v1.ttl",
    )

    chain = OntotextGraphDBQAChain.from_llm(llm, graph=graph, verbose=True, allow_dangerous_requests=True,)
    
    q1 = "What are the data products managed by the domain 'Services'" # gerou query errada = gpt 4 mini e gpt 3.5 turno
    q2 = "Give me the breakdown of data products per domain per data product type" # query correta = gpt 4 mini
    q3 = "What are the data products owned by 'John Doe'" # gerou a query correta mas nao retornou valor na chain
    q4 = "What are the BI Reports across the domain 'Supply Chain'" # gerou query com sintaxe errada no gpt 4 mini e gerou query com sintaxe correta porem com resultado errado no gpt 3.5
    q5 = "List the data products that cover Customer" # Funcionou no gpt 4 mini somente tirando o plural de Customers, ficando o nome exato do conceito.
    q6 = "List the concepts covered by this data product Customer Order" # no gpt 4 mini so funciona com o nome exato do produto - considerar similarity search?
    q7 = "List the data products that share at least one concept with the data product 'Customer Order Data Product'" #gerando query errada tanto no gpt 4 mini quanto no 3.5 turbo
    q8 = "What source data products are used by this data product 'Customer Order Data Product'" #gerando query errada tanto no gpt 4 mini quanto no 3.5 turbo

    res = chain.invoke({chain.input_key: q7})[chain.output_key]
    print(res)
