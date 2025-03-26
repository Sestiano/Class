"""Run this model in Python

> pip install azure-ai-inference
"""
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.ai.inference.models import ImageContentItem, ImageUrl, TextContentItem
from azure.core.credentials import AzureKeyCredential

def chat(user_query):
    # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
  # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
    client = ChatCompletionsClient(
        endpoint = "https://models.inference.ai.azure.com",
        credential = AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
        api_version = "2024-08-01-preview",
    )

    response = client.complete(
    messages = [
        SystemMessage(content = "Generate a single question on a specific topic and accompany it with an answer and a series of progressively specific hints designed to guide students toward the correct solution.\n\n\n# Guidelines\n\n- Ensure the question is clear and suitable for the intended grade level (e.g., elementary, middle school, high school, college). If no grade level is specified, default to a general middle-school level question.\n- Provide hints gradually, starting with broad clues and narrowing down to specific ones.\n- Confirm that the answer aligns perfectly with the question and hints.\n- Only one question should be generated per request.\n\n# Steps\n\n1. **Create the Question**: Choose a topic appropriate for a general or specific audience (e.g., science, history, math). Ensure the question is clear and unambiguous.\n2. **Provide the Answer**: Clearly state the correct answer in detail.\n3. **Design the Hints**: Write a series of 3-5 hints that progressively narrow down to the correct answer. Start with broad, general hints and move toward more specific clues that lead directly to the answer.\n\n# Output Format\n\nThe output should be formatted as follows:\n- **Topic**: [Specify the subject or category]\n- **Question**: [Insert the question here]\n- **Hints**:\n  1. [First general or broad hint]\n  2. [Second, more specific hint]\n  3. [Third, even more specific hint]\n  4. [Optional: Fourth highly specific hint or instruction]\n- **Answer**: [Provide the correct answer here]\n\n# Examples\n\n**Example 1**\n- **Topic**: History  \n- **Question**: Who was the first president of the United States?  \n- **Hints**:  \n  1. He is sometimes referred to as the \"Father of His Country.\"  \n  2. He was the commander-in-chief of the Continental Army during the American Revolutionary War.  \n  3. He served as president from 1789 to 1797.  \n  4. A famous U.S. capital city is named after him.  \n- **Answer**: George Washington  \n\n**Example 2**\n- **Topic**: Science  \n- **Question**: What is the chemical symbol for water?  \n- **Hints**:  \n  1. It is a compound made of two elements commonly found in the periodic table.  \n  2. Its formula includes one oxygen atom.  \n  3. It consists of two hydrogen atoms for each oxygen atom.  \n  4. Its common state in nature is liquid, essential for life.  \n- **Answer**: H₂O  \n\n**Example\n- **Topic**: Chemistry  \n- **Question**: What is the hybridization of the central atom in the molecule sulfur hexafluoride (SF₆)?  \n- **Hints**:  \n  1. The molecule has an octahedral geometry.  \n  2. The central atom in the molecule forms six sigma bonds with surrounding fluorine atoms.  \n  3. The hybrid orbitals involved include one s orbital, three p orbitals, and two d orbitals.  \n  4. The hybridization corresponds to sp³d², commonly associated with octahedral shapes.  \n- **Answer**: The hybridization of the central sulfur atom in SF₆ is **sp³d²**.\n\n**Example 4**\n- **Topic**: Mathematics (Algebra/Functions)  \n- **Question**: Solve for \\( x \\) in the equation \\( 2^{x+1} + 2^x = 48 \\).  \n- **Hints**:  \n  1. Start by factoring out \\( 2^x \\) from both terms on the left-hand side.  \n  2. The equation simplifies to \\( 2^x(2 + 1) = 48 \\).  \n  3. Divide both sides by 3 to isolate \\( 2^x \\).  \n  4. Use the property of logarithms to solve for \\( x \\): \\( x = \\log_2(\\text{value}) \\).  \n- **Answer**: Factoring \\( 2^x \\), the equation becomes \\( 2^x \\cdot 3 = 48 \\), so \\( 2^x = 16 \\). Converting \\( 16 \\) to a power of 2 gives \\( 2^4 \\). Therefore, \\( x = 4 \\).\n\n# Notes\n\n- Ensure hints are neither too vague nor too explicit initially to maintain a logical progression.\n- Avoid repetition or redundancy in the clues.\n- Tailor the difficulty of the question and hints to the target age or knowledge level of the audience."),
        UserMessage(content = [
            TextContentItem(text = "Create a hard chemistry question for advanced high school students."),
        ]),
        AssistantMessage(content = "- **Topic**: Chemistry  \n- **Question**: What is the hybridization of the central atom in the molecule sulfur hexafluoride (SF₆)?  \n- **Hints**:  \n  1. The molecule has an octahedral geometry.  \n  2. The central atom in the molecule forms six sigma bonds with surrounding fluorine atoms.  \n  3. The hybrid orbitals involved include one s orbital, three p orbitals, and two d orbitals.  \n  4. The hybridization corresponds to sp³d², commonly associated with octahedral shapes.  \n- **Answer**: The hybridization of the central sulfur atom in SF₆ is **sp³d²**."),
        UserMessage(content = [
            TextContentItem(text = "Create a hard math question for advanced high school students."),
        ]),
        AssistantMessage(content = "- **Topic**: Mathematics (Algebra/Functions)  \n- **Question**: Solve for \\( x \\) in the equation \\( 2^{x+1} + 2^x = 48 \\).  \n- **Hints**:  \n  1. Start by factoring out \\( 2^x \\) from both terms on the left-hand side.  \n  2. The equation simplifies to \\( 2^x(2 + 1) = 48 \\).  \n  3. Divide both sides by 3 to isolate \\( 2^x \\).  \n  4. Use the property of logarithms to solve for \\( x \\): \\( x = \\log_2(\\text{value}) \\).  \n- **Answer**: Factoring \\( 2^x \\), the equation becomes \\( 2^x \\cdot 3 = 48 \\), so \\( 2^x = 16 \\). Converting \\( 16 \\) to a power of 2 gives \\( 2^4 \\). Therefore, \\( x = 4 \\)."),
        UserMessage(content = [
            TextContentItem(text = "generate a question about the process of photosynthesis"),
        ]),
    ],
        model = "gpt-4o",
        response_format = "text",
        max_tokens = 4096,
        temperature = 1,
        top_p = 1,
    )

    print(response.choices[0].message.content)

def main():
    print("Enter your query (type 'exit' to quit):")
    
    while True:
        user_input = input("> ")
        
        if user_input.lower() == 'exit':
            break
            
        try:
            chat(user_input)
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()