#
# https://weaviate.io/developers/weaviate/search/generative
#

WEAVIATE_CLASS = "Document"
WEAVIATE_SCHEMA = {
    "classes": [
        {
            "class": WEAVIATE_CLASS,
            "description": "LangChain Documents",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text"
                },
                "generative-openai": {
                    "model": "gpt-4",
                }
            },
            "properties": [
                {
                    "dataType": ["text"],
                    "description": "The Content of the LangChain Document",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False,
                        }
                    },
                    "name": "content",
                },
            ],
        },
    ]
}
