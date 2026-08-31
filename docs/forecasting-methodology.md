# Forecasting Methodology and Planning Semantics

This is a high-level methodology overview. It deliberately omits company data, selected model assignments, scores, registry contents, and private feature definitions.

**Case-study map:** [Overview](../README.md) | [Architecture](architecture.md) | [Governance and release](governance-and-release.md)

## Revenue model evaluation

The system evaluates candidate forecasting approaches by brand using leakage-safe, time-aware backtesting. This means each historical test period is evaluated using only information that would have been available at that point in time.

Selection considers more than a single error score:

- accuracy across the defined evaluation windows;
- stability across forecast horizons;
- operational practicality;
- interpretability for planning users; and
- repeatability under governed release rules.

One method is selected and frozen for each brand. A routine data refresh can create a new forecast run, but it does not silently redefine the official method.

## Wholesale as planning context

Vehicle Wholesale provides an important planning driver and denominator. The system preserves the distinction between an explicit planned zero and an unavailable input. When approved plans are unavailable, governed fallback logic is documented and visible rather than hidden inside a model result.

Regular PNVW is regular accessory Revenue divided by selected regular Wholesale vehicles. It is a per-vehicle Revenue context metric, not an all-in metric that absorbs separately governed Fleet activity.

## Current-month nowcasting

For the current incomplete month, month-to-date information is used to update the near-term view. The result is labeled a Nowcast. Completed historical months remain Actual, and future periods remain Forecast.

## Hierarchical planning

Planning consumers need information at several levels:

```text
Total -> Brand -> Vehicle Model -> PLC / Accessory Category
```

The system uses the approved brand-level Revenue forecast as the control total. Lower-level Quantity signals and historical category patterns are then reconciled to support operational model and PLC planning. This avoids presenting independently generated lower-level figures that do not add up to the approved business view.

## Separate business components

Some program components require their own business treatment. The system keeps such a component separate from regular business metrics, adds it once to the all-in outlook, and avoids attributing it to a vehicle model without a governed basis. This is important for preventing double counting and misleading per-vehicle context.

**Next:** [Governance, QA, and approved-release lifecycle](governance-and-release.md)
