# Lara Payment Plan Python SDK

This is the Lara Payment Plan SDK, the core of the Lara Credit Proposal System.

## About

This SDK, like other Lara Payment Plan SDKs, is a wrapper around the Lara Payment Plan Rust library.
The calculations are performed by the bundled native library inside `payment_plan/_internal`.
Currently, the library is available for Linux and Windows. MacOS support is planned for the future.

## Installation

Install from PyPI:

```bash
pip install payment-plan-python-sdk
```

The SDK depends on bundled native binaries. If your environment blocks binary loading, make sure your runtime allows loading shared libraries.

## Usage

```python
from datetime import datetime, timedelta, timezone
from payment_plan import (
	Params,
	DownPaymentParams,
	calculate_payment_plan,
	calculate_down_payment_plan,
	disbursement_date_range,
	get_non_business_days_between,
	next_disbursement_date,
)
```

### calculate_payment_plan

Calculates payment plans without down payment given a `Params` object.

Returns a `list[Response]` with plans from 1 installment up to the requested number of installments.
Plans whose `installment_amount` are below `min_installment_amount` are not included.

```python
from datetime import datetime, timedelta, timezone
from payment_plan import Params, calculate_payment_plan

params = Params(
	requested_amount=7800,
	first_payment_date=datetime(2025, 5, 3, tzinfo=timezone(timedelta(hours=-3))),
	disbursement_date=datetime(2025, 4, 5, tzinfo=timezone(timedelta(hours=-3))),
	installments=4,
	debit_service_percentage=0,
	mdr=0.05,
	tac_percentage=0,
	iof_overall=0.0038,
	iof_percentage=0.000082,
	interest_rate=0.0235,
	min_installment_amount=100,
	max_total_amount=1_000_000,
	disbursement_only_on_business_days=True,
	min_installments=None,
)

plans = calculate_payment_plan(params)
print(len(plans), plans[0].installment_amount)
```

Parameters:

- `requested_amount`: Requested principal amount.
- `first_payment_date`: First due date of the plan.
- `disbursement_date`: Date when funds are disbursed.
- `installments`: Maximum number of installments to evaluate.
- `debit_service_percentage`: Debit service percentage.
- `mdr`: Merchant Discount Rate.
- `tac_percentage`: TAC percentage.
- `iof_overall`: Overall IOF value.
- `iof_percentage`: Daily IOF percentage.
- `interest_rate`: Monthly interest rate.
- `min_installment_amount`: Minimum allowed installment amount.
- `max_total_amount`: Maximum allowed total amount.
- `disbursement_only_on_business_days`: Restrict disbursement to business days.
- `min_installments`: Optional minimum installment number to include in results.

Errors:

- If `requested_amount` is less than or equal to 0.
- If `installments` is less than or equal to 0.
- If date fields are invalid.
- If tax/interest parameters are incompatible with the internal XIRR-based calculation.

### calculate_down_payment_plan

Calculates payment plans with down payment given a `DownPaymentParams` object.

Returns a `list[DownPaymentResponse]` with down-payment options from 1 installment up to the requested installment count.

```python
from datetime import datetime, timedelta, timezone
from payment_plan import Params, DownPaymentParams, calculate_down_payment_plan

base_params = Params(
	requested_amount=7800,
	first_payment_date=datetime(2025, 5, 3, tzinfo=timezone(timedelta(hours=-3))),
	disbursement_date=datetime(2025, 4, 5, tzinfo=timezone(timedelta(hours=-3))),
	installments=4,
	debit_service_percentage=0,
	mdr=0.05,
	tac_percentage=0,
	iof_overall=0.0038,
	iof_percentage=0.000082,
	interest_rate=0.0235,
	min_installment_amount=100,
	max_total_amount=1_000_000,
	disbursement_only_on_business_days=True,
	min_installments=None,
)

down_payment_params = DownPaymentParams(
	first_payment_date=datetime(2025, 5, 3, tzinfo=timezone(timedelta(hours=-3))),
	requested_amount=1000,
	installments=4,
	min_installment_amount=100,
	params=base_params,
)

down_payment_plans = calculate_down_payment_plan(down_payment_params)
print(down_payment_plans[0].installment_quantity)
```

Parameters:

- `requested_amount`: Down payment amount.
- `min_installment_amount`: Minimum installment amount for down payment options.
- `installments`: Maximum number of down payment installments to evaluate.
- `first_payment_date`: First due date for the down payment plan.
- `params`: A `Params` object used for the main payment plan calculation.

Errors:

- If `requested_amount` is less than or equal to 0.
- If `installments` is less than or equal to 0.
- If date fields are invalid.
- If tax/interest parameters are incompatible with the internal XIRR-based calculation.

### disbursement_date_range

Calculates start and end dates for a disbursement period based on a `base_date` and number of business days.

```python
from datetime import datetime, timezone
from payment_plan import disbursement_date_range

base_date = datetime(2078, 2, 12, tzinfo=timezone.utc)
days = 5
start_date, end_date = disbursement_date_range(base_date, days)
print(start_date, end_date)
```

Parameters:

- `base_date`: Base date used to calculate the business-day range.
- `days`: Number of business days to include.

Returns:

- A tuple `(start_date, end_date)`.

Errors:

- If `base_date` is invalid.

### get_non_business_days_between

Returns non-business days (weekends and bank holidays) between two dates, inclusive.

```python
from datetime import datetime, timezone
from payment_plan import get_non_business_days_between

start_date = datetime(2078, 11, 12, tzinfo=timezone.utc)
end_date = datetime(2078, 11, 22, tzinfo=timezone.utc)
non_business_days = get_non_business_days_between(start_date, end_date)
print(non_business_days)
```

Parameters:

- `start_date`: Start date of the interval.
- `end_date`: End date of the interval.

Returns:

- A list of non-business dates between `start_date` and `end_date`.

Errors:

- If `start_date` or `end_date` is invalid.
- If `start_date` is after `end_date`.

### next_disbursement_date

Calculates the next valid disbursement date based on `base_date`.

```python
from datetime import datetime, timezone
from payment_plan import next_disbursement_date

base_date = datetime(2078, 2, 12, tzinfo=timezone.utc)
result = next_disbursement_date(base_date)
print(result)
```

Parameters:

- `base_date`: Base date used for the calculation.

Returns:

- The next valid disbursement date.

Errors:

- If `base_date` is invalid.

Warning:
As of now, if `base_date` is the same calendar day as "today", this day is considered invalid for disbursement and the function returns the next valid date.

## Contributing

This repository and the code in it are a mirror of the code on [Parcelado Lara Payment Plan](https://github.com/ParceladoLara/payment-plan).
To contribute, open contributions in the main payment-plan repository. Changes are reflected here after release.

## License

This software is provided free of charge for personal or internal business use only.
Modification, redistribution, sublicensing, or reverse engineering is not permitted.
Copyright (c) 2025 SWEETPAY SOLUCOES FINANCEIRAS LTDA. All rights reserved.
