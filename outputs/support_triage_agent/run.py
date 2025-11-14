from agent import GeneratedAgent
import argparse, json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_path", type=str, required=False, help="Path to input file")
    parser.add_argument("--support_path", type=str, required=False, help="Path to support text")
    parser.add_argument("--csv_path", type=str, required=False, help="Path to CSV")
    args = parser.parse_args()

    agent = GeneratedAgent()
    ctx = agent.run(
        pdf_path=args.pdf_path,
        support_path=args.support_path,
        csv_path=args.csv_path
    )
    print(json.dumps(ctx, indent=2))
