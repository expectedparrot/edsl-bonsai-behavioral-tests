"""Ask the Linda question through EDSL; automatically manage the local server."""

from pathlib import Path

from edsl import Cache, Model, QuestionMultipleChoice
from edsl.config import CONFIG

from bonsai_server import BASE_URL, bonsai_server


def main():
    CONFIG.EDSL_API_TIMEOUT = "300"
    model = Model(
        "bonsai-2-27b",
        service_name="openai_compatible",
        base_url=f"{BASE_URL}/v1",
        temperature=1.0,
        top_p=0.95,
        max_tokens=2048,
    )
    question = QuestionMultipleChoice(
        question_name="linda",
        question_text=(
            "Linda is 31 years old, single, outspoken, and very bright. "
            "She majored in philosophy. As a student, she was deeply concerned "
            "with issues of discrimination and social justice, and also "
            "participated in anti-nuclear demonstrations. Which is more probable?"
        ),
        question_options=[
            "Linda is a bank teller.",
            "Linda is a bank teller and is active in the feminist movement.",
        ],
    )
    with bonsai_server():
        results = question.by(model).run(
            disable_remote_inference=True,
            disable_remote_cache=True,
            cache=Cache(),
            stop_on_exception=True,
        )
    answer = results.select("answer.linda").first()
    if answer is None:
        raise RuntimeError("Bonsai returned no answer; inspect managed-server.log.")
    output = Path(__file__).resolve().parent / "runs" / "linda.results.ep"
    output.parent.mkdir(parents=True, exist_ok=True)
    results.save(str(output))
    print(answer)
    print(f"Saved results to {output}")
    return results


if __name__ == "__main__":
    main()
