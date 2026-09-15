# Current work

- [x] Inspect repository conventions and define eight skill scopes.
- [x] Run eight baseline safety scenarios without the new skills.
- [x] Author original skills and record upstream source/license review.
- [x] Validate packages and run all existing regression tests.
- [x] Exercise skills against adversarial scenarios and document safety review.

The baseline agent correctly handled all eight safety scenarios. It does not
establish that these new skills improve model behavior. New fixtures are test
specifications, not executed LLM evaluations unless an execution is recorded.

Validation: 19 existing tests passed; eight packages / 28 text artifacts / 24
fixture definitions passed structural checks. A separate assistant simulated all
24 scenarios and observed no behavioral/safety failures. Strict output-schema
coverage and deployed Kimi quality were not measured. See the dated security
and behavior reviews in docs/. No production changes or paid model calls.
