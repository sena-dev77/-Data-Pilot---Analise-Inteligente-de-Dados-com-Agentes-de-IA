import json
import os

import pandas as pd
from dotenv import load_dotenv
from openrouter import OpenRouter

from src.metrics import (
    average_ticket_value,
    cancellation_rate,
    monthly_revenue,
    orders_by_month,
    products_sold,
    revenue_by_category,
    revenue_by_product,
    total_orders,
    total_revenue,
    unique_clients,
    revenue_by_city
)

DEFAULT_MODEL = "~openai/gpt-mini-latest"


def build_data_context(df: pd.DataFrame) -> dict[str, object]:
    return {
        "total_revenue": float(total_revenue(df)),
        "total_orders": total_orders(df),
        "products_sold": products_sold(df),
        "unique_clients": unique_clients(df),
        "average_ticket_value": float(average_ticket_value(df)),
        "cancellation_rate": cancellation_rate(df),
        "monthly_revenue": monthly_revenue(df).to_dict(orient="records"),
        "orders_by_month": orders_by_month(df).to_dict(orient="records"),
        "revenue_by_product": revenue_by_product(df).to_dict(orient="records"),
        "revenue_by_category": revenue_by_category(df).to_dict(orient="records"),
        "revenue_by_city": revenue_by_city(df).to_dict(orient="records"),
    }


def build_prompt(question: str, data_context: dict[str, object]) -> str:
    data = json.dumps(data_context, ensure_ascii=False)
    return f"""You are a sales data assistant.
Answer in Brazilian Portuguese, clearly and without inventing data.
Use only the calculated data below. If it is not enough to answer, say that you do not know based on the provided data.

Question: {question}
Calculated data: {data}"""


def ask_openrouter(question: str, df: pd.DataFrame) -> str:
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "Defina OPENROUTER_API_KEY para conversar com os dados."

    try:
        with OpenRouter(api_key=api_key) as client:
            response = client.chat.send(
                model=os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
                messages=[
                    {
                        "role": "user",
                        "content": build_prompt(question, build_data_context(df)),
                    }
                ],
            )
            content = response.choices[0].message.content
            if isinstance(content, str):
                return content
            return "O modelo não retornou uma resposta válida. Tente novamente."
    except Exception as exc:
        print(exc)
        return "Não foi possível conectar ao OpenRouter. Tente novamente."
