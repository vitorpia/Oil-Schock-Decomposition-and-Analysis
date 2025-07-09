# 📊 Oil Shocks Indexes (ODS, OSS, ORS)

**Description**:  
This repository provides a fully reproducible Python pipeline to construct three oil price shock indexes — **ODS (Oil Demand Shock)**, **OSS (Oil Supply Shock)**, and **ORS (Oil Risk Shock)** — based on Brent prices, macroeconomic activity, and volatility data. The methodology is inspired by macro-financial literature and uses freely available APIs (Yahoo Finance and FRED).

---

## 🧭 Background and Motivation

The decomposition of oil price shocks into **demand**, **supply**, and **risk-based** components was first formalized by **Lutz Kilian (2009)** in *“Not All Oil Price Shocks Are Alike: Disentangling Demand and Supply Shocks in the Crude Oil Market”*. Later, **Caldara, Cavallo, and Iacoviello (2019)** advanced the identification using high-frequency methods.

In this repository, we adopt a transparent, monthly-resolution framework to replicate those concepts. The three indexes are constructed as:

- **ODS (Oil Demand Shock)** – portion of oil returns explained by industrial production (global demand).
- **OSS (Oil Supply Shock)** – residual component not explained by demand, often linked to disruptions.
- **ORS (Oil Risk Shock)** – conditional volatility (GARCH) of oil returns, capturing market uncertainty.

These indexes are important tools in:
- Forecasting the macroeconomic impact of oil shocks,
- Identifying whether a shock is inflationary or growth-inducing,
- Supporting central bank, fiscal, and geopolitical analysis.

---

## 📅 Period Covered

The dataset covers monthly data from **January 2000 to December 2024**, depending on availability.

---

## 📦 Data Sources

- 📈 Brent crude prices: Yahoo Finance (`BZ=F`)
- 🌍 Global economic activity: `INDPRO` from FRED (used as a proxy for world IPM)
- 📉 Oil volatility index: Yahoo Finance (`^OVX`)
- 📊 GARCH(1,1) volatility: Estimated from daily log returns of Brent

---

## 🧪 Methodology

1. **Download daily Brent prices** and compute monthly log-returns.
2. **Download OVX (volatility)** and average monthly values.
3. **Download INDPRO (Industrial Production)** from FRED as a global demand proxy.
4. **Estimate GARCH(1,1)** on daily returns to compute conditional volatility.
5. **OLS Regression** of Brent returns on INDPRO to separate demand and supply components.
6. Final construction of:
   - `ODS`: fitted values from OLS (demand shock),
   - `OSS`: residuals from OLS (supply shock),
   - `ORS`: GARCH-based conditional volatility (risk shock).

---

📂 Outputs
After running the pipeline, the final DataFrame includes the following columns:

brent_ret: Monthly log-return of Brent crude oil prices.

ipm: Industrial production proxy from FRED.

vol_garch: Conditional volatility estimated via GARCH(1,1).

OVX: Monthly average of the Oil Volatility Index.

ODS: Oil Demand Shock (fitted values from OLS).

OSS: Oil Supply Shock (residuals from OLS).

ORS: Oil Risk Shock (volatility-based).

---

👤 Author
Developed by Vitor Piagetti Aimi, economist, data scientist and engineer, with research interests in macro-financial modeling, international economics, and statistical learning. Inspired by academic works of Kilian (2009) and Caldara et al. (2019).

--

📄 License
This project is licensed under the MIT License — see the LICENSE file for details.
