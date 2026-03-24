from __future__ import annotations

import argparse
from pathlib import Path

from quote_core.app.calculate_quote import calculate_quote
from quote_core.domain.models import QuoteRequest


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate laser cutting quote from DXF."
    )
    parser.add_argument("dxf_file", type=Path, help="Path to DXF file")
    parser.add_argument(
        "--material-code",
        type=str,
        default="steel_s235",
        help="Material code from catalogs/materials.py",
    )
    parser.add_argument(
        "--thickness-mm",
        type=float,
        default=2.0,
        help="Sheet thickness in millimeters",
    )
    parser.add_argument(
        "--quantity",
        type=int,
        default=1,
        help="Part quantity",
    )
    return parser


def main() -> None:
    parser = _build_cli_parser()
    args = parser.parse_args()

    request = QuoteRequest(
        dxf_path=str(args.dxf_file),
        material_code=args.material_code,
        thickness_mm=args.thickness_mm,
        quantity=args.quantity,
    )

    result = calculate_quote(request)
    print(f"Total price: {result.costs.total_cost:.2f} RUB")
    print(
        "Breakdown:",
        (
            f"material={result.costs.material_cost:.2f}, "
            f"cutting={result.costs.cutting_cost:.2f}, "
            f"piercing={result.costs.piercing_cost:.2f}, "
            f"setup={result.costs.setup_cost:.2f}"
        ),
    )


if __name__ == "__main__":
    main()
