import json
from pathlib import Path
from collections import defaultdict
import typer
import inspect

from evaluators import MyEvaluator
from utils.crosswalk_loader import CrosswalkLoader
import scoring
from weights import WEIGHTS

app = typer.Typer()

def evaluate_file(codemeta_path: Path) -> dict:
    evaluator = MyEvaluator(codemeta_path)
    codemeta_json = evaluator.validate_codemeta_file()
    crosswalk = CrosswalkLoader(codemeta_json)
    eval_mapping = crosswalk.map_evaluators_to_codemeta()
    model_name = codemeta_json["name"]

    eval_results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    eval_method_names = [
        name for name in dir(evaluator)
        if name.startswith("eval") and callable(getattr(evaluator, name))
    ]

    for method_name in eval_method_names:
        method = getattr(evaluator, method_name)
        indicator = method_name[4:]

        try:
            result, log = method(**eval_mapping[method_name])
        except KeyError:
            expected_args = inspect.signature(method).parameters
            result = False
            log = [f"Missing inputs {list(expected_args.keys())} for {method_name}"]
        
        eval_results[model_name]["indicator_evaluations"][indicator]["result"] = result
        eval_results[model_name]["indicator_evaluations"][indicator]["log"] = log

    eval_results[model_name]["scores"] = scoring.compute_indicator_scores(
        eval_results[model_name]["indicator_evaluations"], WEIGHTS
    )
    return eval_results

@app.command()
def evaluate(
    file: Path = typer.Option(None, "--file", "-f", exists=True, file_okay=True, dir_okay=False),
    directory: Path = typer.Option(None, "--directory", "-d", exists=True, file_okay=False, dir_okay=True),
    output: Path = typer.Option(None, "--output", "-o", file_okay=False, dir_okay=True),
    verbose: bool = typer.Option(False, "--verbose", "-v")
):
    """
    Evaluate one CodeMeta file or all files in a directory.
    """

    if (file is None and directory is None) or (file and directory):
        typer.echo("Error: Provide exactly one of --file or --directory.", err=True)
        raise typer.Exit(code=1)

    if output:
        output.mkdir(parents=True, exist_ok=True)

    if file:
        if verbose:
            typer.echo(f"Evaluating file: {file}")
        result = evaluate_file(file)

        if output:
            outfile = output / f"{file.stem}.json"
            with open(outfile, "w") as f_out:
                json.dump(result, f_out, indent=2)
            typer.echo(f"Results saved to: {outfile}")
        else:
            typer.echo(json.dumps(result, indent=2))

    elif directory:
        json_files = list(directory.glob("*.json"))
        output.mkdir(parents=True, exist_ok=True) if output else None

        for i, f in enumerate(json_files, 1):
            if verbose:
                typer.echo(f"[{i}/{len(json_files)}] Evaluating {f.name}")
            result = evaluate_file(f)

            if output:
                outfile = output / f"{f.stem}.json"
                with open(outfile, "w") as f_out:
                    json.dump(result, f_out, indent=2)
                typer.echo(f"Saved to {outfile}")
            else:
                typer.echo(json.dumps(result, indent=2))



if __name__ == "__main__":
    app()


