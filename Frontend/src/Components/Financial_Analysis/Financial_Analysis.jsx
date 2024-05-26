import React, { useState } from "react";
import Loader from "../Loader/Loader";
import { stylings } from "../../UTILS/UTILS_STYLES";
import { globalContext } from "../../Context/Context";
import RenderForm from "./RenderForm";
import SVGComponent from "../SVGS/SVGS";
import { makeApiRequest } from "../../UTILS/UTILS_HELPERS";
import toast from "react-hot-toast";
import Results from "./Results";
import ToolTip from "../NumbersData/ToolTip";
export default function FinancialAnalysis({ bessCost, bessPower }) {
  const { theme } = React.useContext(globalContext);
  const errorsInitialState = {
    projectDebt: {
      debt_percent: false,
      debt_term: false,
      debt_interest_rate: false,
    },
    reserveAccounts: {
      reserveAmount: false,
      interestRate: false,
    },
    utilityBill: {
      averageDemandRate: false,
      averageEnergyRate: false,
      monthlyFixedAmount: false,
    },
    initialInvestment: {
      project_length: false,
      bessCost: false,
      differential: false,
      initial_investment: false,
    },
    investmentTaxCredit: {
      fedral: false,
    },
    taxes: {
      fed_tax_rate: false,
      state_tax_rate: false,
      insurance_rate: false,
      salesTax: false,
      property_tax_rate: false,
      AssedssedValue: false,
      property_assessed_pct: false,
    },
    capacityPayments: {
      commitmentAmount: false,
      commitmentPayment: false,
    },
  };
  const [loaded, setLoaded] = useState(false);
  const [results, setResults] = React.useState({
    npv: 100000,
    irr: 14,
    payback_period: 4,
    lcoe: 0.15,
    itc: 145125,
    year1_bill_savings: 29825,
    dr_capacity_revenue: 34850,
  });
  const renderResultsHelper = [
    {
      label: "Payback Time",
      accessor: "payback_period",
      backLabel: " Years",
      tooltip: "",
    },
    {
      label: "NPV",
      accessor: "npv",
      tooltip:
        "Measures a project's economic feasibility using both revenue/ savings and costs. In general, a project with a positive NPV is economically feasible, while one with a negative NPV is not.",
    },
    {
      label: "DR Revenue",
      accessor: "dr_capacity_revenue",
      tooltip:
        "Revenue earned from participating in demand response programs. DR Revenue = Capacity Payment ($/kW) * BESS Capacity Committed (kW)",
    },
    {
      label: "IRR",
      accessor: "irr",
      backLabel: " / %",
      tooltip: "",
    },
    {
      label: "ITC",
      accessor: "itc",
      tooltip:
        "Federal Investment Tax Credit. The rate can start at 30% and increase based on various factors.",
    },
    {
      label: "1 Year Bill Savings",
      accessor: "year1_bill_savings",
      tooltip:
        "Difference between the utility bill payment with and without the BESS. Using the 1st year energy values for the project.",
    },
    {
      label: "LCOE",
      accessor: "lcoe",
      backLabel: " $/kWh",
      tooltip:
        "The average cost per unit of energy produced, calculated over the lifetime of the battery.",
    },
  ];
  const [selectedForm, setSelectedForm] = useState();
  const [errors, setErrors] = React.useState(
    JSON.parse(JSON.stringify(errorsInitialState))
  );
  const [state, setState] = React.useState({
    differential: "",
    projectDebt: {
      debt_percent: { value: 30, selectedMeasureUnit: "%" },
      debt_term: 18,
      debt_interest_rate: 6,
    },
    initialInvestment: {
      project_length: { value: 20, selectedMeasureUnit: "years" },
      bessCost: bessCost,
      differential: { value: 30, selectedMeasureUnit: "%" },
      initial_investment: bessCost + 1300,
    },
    reserveAccounts: {
      reserveAmount: { value: 30, selectedMeasureUnit: "%" },
      interestRate: 1.5,
    },
    utilityBill: {
      averageDemandRate: 20,
      averageEnergyRate: 5,
      monthlyFixedAmount: 200,
    },
    investmentTaxCredit: {
      fedral: {
        value: 30,
        selectedMeasureUnit: "%",
      },
    },
    taxes: {
      fed_tax_rate: 21,
      state_tax_rate: 7,
      insurance_rate: 0.25,
      salesTax: 8,
      property_tax_rate: 3,
      AssedssedValue: 4000,
      property_assessed_pct: 100,
    },
    capacityPayments: {
      commitmentAmount: { value: 30, selectedMeasureUnit: "$" },
      commitmentPayment: { value: 30, selectedMeasureUnit: "kW" },
    },
    demandResponse: {
      inputs: {
        January: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        February: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        March: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        April: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        May: {
          CommitmentAmount: 50,
          CommitmentPayment: 143,
          totalDrPayment: 7150,
        },
        June: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        July: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        August: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        September: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        October: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        November: {
          CommitmentAmount: 50,
          CommitmentPayment: 43,
          totalDrPayment: 2150,
        },
        December: {
          CommitmentAmount: 50,
          CommitmentPayment: 143,
          totalDrPayment: 7150,
        },
      },
      selectedCommetmentAmount: "%",
    },
  });
  React.useEffect(() => {
    if (bessCost) {
      setLoaded(false);
      let initial_investment = 0;
      console.log({ what: state.initialInvestment.differential.value });
      if (state.initialInvestment.differential.selectedMeasureUnit === "$") {
        initial_investment =
          bessCost + state.initialInvestment.differential.value;
      } else {
        initial_investment =
          bessCost +
          (state.initialInvestment.differential.value / 100) * bessCost;
      }
      const updatedState = {
        ...state,
        initialInvestment: {
          ...state.initialInvestment,
          bessCost: bessCost,
          initial_investment: initial_investment,
        },
      };
      console.log({ updatedState, bessCost });
      setState({ ...updatedState });

      const debt_percent = +state.projectDebt.debt_percent.value;
      const optimisedPayload = {
        energy_payment: +state.utilityBill.averageEnergyRate,
        demand_payment: +state.utilityBill.averageDemandRate,
        fixed_payment: +state.utilityBill.monthlyFixedAmount,
        project_length: +state.initialInvestment.project_length.value,
        initial_investment: +updatedState.initialInvestment.initial_investment,
        debt_percent:
          state.projectDebt.debt_percent.selectedMeasureUnit === "%"
            ? debt_percent
            : (debt_percent /
                +updatedState.initialInvestment.initial_investment) *
              100,
        debt_interest_rate: +state.projectDebt.debt_interest_rate,
        debt_term: +state.projectDebt.debt_term,
        property_tax_rate: +state.taxes.property_tax_rate,
        property_assessed_pct: +state.taxes.property_assessed_pct,
        fed_tax_rate: +state.taxes.fed_tax_rate,
        state_tax_rate: +state.taxes.state_tax_rate,
        insurance_rate: +state.taxes.insurance_rate,
      };
      makeApiRequest({
        method: "post",
        urlPath: "Fancial_Analysis",
        body: { ...optimisedPayload },
      })
        .then(({ data, error }) => {
          if (error) {
            toast.error("Something went wrong");
          } else {
            setResults({ ...data.data });
            setLoaded(true);
            // console.log({data : {...data.data}})
          }
        })
        .catch(() => {
          toast.error("Something went wrong");
        });
    }
  }, [bessCost]);
  React.useEffect(() => {
    const demandResponse = state.demandResponse.inputs;
    Object.keys(demandResponse).map((val) => {
      if (state.demandResponse.selectedCommetmentAmount === "%") {
        demandResponse[val].totalDrPayment =
          (demandResponse[val].CommitmentAmount / 100) *
          bessPower *
          demandResponse[val].CommitmentPayment;
      } else {
        demandResponse[val].totalDrPayment =
          demandResponse[val].CommitmentAmount *
          demandResponse[val].CommitmentPayment;
      }
    });
    let initial_investment = 0;
    console.log({ what: state.initialInvestment.differential.value });
    if (state.initialInvestment.differential.selectedMeasureUnit === "$") {
      initial_investment =
        bessCost + state.initialInvestment.differential.value;
    } else {
      initial_investment =
        bessCost +
        (state.initialInvestment.differential.value / 100) * bessCost;
    }
    console.log({ initial_investment });
    const updatedState = {
      ...state,
      initialInvestment: {
        ...state.initialInvestment,
        bessCost: bessCost,
        initial_investment: initial_investment,
      },
      demandResponse: {
        ...state.demandResponse,
        inputs: { ...demandResponse },
      },
    };
    setState({ ...updatedState });
    console.log({ bessPower, bessCost }, "this is to debug");
  }, [bessPower]);
  const [formHelpers, setFormHelpers] = React.useState({
    projectDebt: {
      label: "Project Debt",
      accessor: "projectDebt",
      fields: [
        {
          label: "DEBT Amount",
          accessor: "debt_percent",
          multipleMeasureUnits: ["%", "$"],
        },
        { label: "Loan Term", accessor: "debt_term" },
        { label: "Loan Rate", accessor: "debt_interest_rate" },
      ],
    },
    initialInvestment: {
      label: "Total Initial Investment",
      accessor: "initialInvestment",
      fields: [
        {
          label: "Project Length",
          accessor: "project_length",
          multipleMeasureUnits: ["Days", "Years"],
        },
        {
          label: "BESS Cost",
          accessor: "bessCost",
          readOnly: true,
        },
        {
          label: "Differential",
          accessor: "differential",
          multipleMeasureUnits: ["%", "$"],
          onChange: (e) => {
            let initial_investment = 0;
            if (
              state.initialInvestment.differential.selectedMeasureUnit === "$"
            ) {
              initial_investment = bessCost + e.target.value;
            } else {
              initial_investment = bessCost + (e.target.value / 100) * bessCost;
            }
            console.log({ stateGot: state.initialInvestment, state });
            // const updatedState = { ...state, initialInvestment: { ...state.initialInvestment, initial_investment: initial_investment , differential : {...state.initialInvestment.differential , value : +e.target.value}}}
            // setState({...updatedState});
          },
          onOptionChange: (e) => {
            let initial_investment = 0;
            if (e.target.value === "$") {
              initial_investment =
                bessCost + state.initialInvestment.differential.value;
            } else {
              initial_investment =
                bessCost +
                (state.initialInvestment.differential.value / 100) * bessCost;
            }
            const updatedState = {
              ...state,
              initialInvestment: {
                ...state.initialInvestment,
                initial_investment: initial_investment,
                differential: {
                  ...state.initialInvestment.differential,
                  selectedMeasureUnit: e.target.value,
                },
              },
            };
            setState({ ...updatedState });
          },
        },
        {
          label: "Total",
          accessor: "initial_investment",
          readOnly: true,
        },
      ],
    },
    reserveAccounts: {
      label: "Reserve Accounts",
      accessor: "reserveAccounts",
      fields: [
        {
          label: "Reserve Amount",
          accessor: "reserveAmount",
          multipleMeasureUnits: ["%", "$"],
        },
        {
          label: "Interest Rate",
          accessor: "interestRate",
        },
      ],
    },
    utilityBill: {
      label: "Utility Bill",
      accessor: "utilityBill",
      fields: [
        {
          label: "Average Demand Rate",
          accessor: "averageDemandRate",
        },
        {
          label: "Average Energy Rate",
          accessor: "averageEnergyRate",
        },
        {
          label: "Monthly Fixed Amount",
          accessor: "monthlyFixedAmount",
        },
      ],
    },
    investmentTaxCredit: {
      label: "Investment Tax Credit",
      accessor: "investmentTaxCredit",
      fields: [
        {
          label: "Fedral",
          accessor: "fedral",
          multipleMeasureUnits: ["%", "$"],
        },
      ],
    },
    taxes: {
      label: "Taxes",
      accessor: "taxes",
      fields: [
        {
          label: "Fedral Income Tax",
          accessor: "fed_tax_rate",
        },
        {
          label: "State Income Tax",
          accessor: "state_tax_rate",
        },
        {
          label: "Insurance Rate",
          accessor: "insurance_rate",
        },
        {
          label: "Sales Tax",
          accessor: "salesTax",
        },
        {
          label: "Property Tax",
          accessor: "property_tax_rate ",
        },
        {
          label: "Assessed Value",
          accessor: "AssedssedValue",
        },
        {
          label: "Assessed Percent",
          accessor: "property_assessed_pct",
        },
      ],
    },
    capacityPayments: {
      label: "Capacity Payments",
      accessor: "capacityPayments",
      fields: [
        {
          label: "Commitment Amount",
          accessor: "commitmentAmount",
          multipleMeasureUnits: ["%", "kW"],
        },
        {
          label: "Commitment Payment",
          accessor: "commitmentPayment",
          multipleMeasureUnits: ["kW", "$"],
        },
      ],
    },
    demandResponse: {
      label: "Demand Response",
      accessor: "demandResponse",
      fields: [
        {
          label: "January",
          accessor: "January",
        },
        {
          label: "February",
          accessor: "February",
        },
        {
          label: "March",
          accessor: "March",
        },
        {
          label: "April",
          accessor: "April",
        },
        {
          label: "May",
          accessor: "May",
        },
        {
          label: "June",
          accessor: "June",
        },
        {
          label: "July",
          accessor: "July",
        },
        {
          label: "August",
          accessor: "August",
        },
        {
          label: "September",
          accessor: "September",
        },
        {
          label: "October",
          accessor: "October",
        },
        {
          label: "November",
          accessor: "November",
        },
        {
          label: "December",
          accessor: "December",
        },
      ],
    },
  });
  const [selectedParameters, setSelectedParameters] = React.useState([]);
  const parameters = [
    {
      label: "Total Initial Investment",
      accessor: "initialInvestment",
      tooltip:
        "The sum of all costs required to start a project, including capital costs, such as the cost of the BESS, installation fees, and financing costs.",
    },
    {
      label: "Project Debt",
      accessor: "projectDebt",
      tooltip:
        "The amount of money borrowed to finance the project, which needs to be repaid over time (debt term) The default percent used is 30% of the initial investment.",
    },
    {
      label: "Reserve Accounts",
      accessor: "reserveAccounts",
      tooltip:
        "Accounts set aside to cover future expenses, emergencies, or maintenance requirements for a project. The percent of initial investment set aside is the reserve percent which is default to 10%. The interest rate the reserve account earns is the reserve interest, defaulted to 1.5%.",
    },
    {
      label: "Utility Bill",
      accessor: "utilityBill",
      tooltip:
        "A statement of the amount owed for electricity, gas, water, or other utility services used over a billing period.",
    },
    {
      label: "Investment Tax Credit",
      accessor: "investmentTaxCredit",
      tooltip: "",
    },
    {
      label: "Taxes",
      accessor: "taxes",
      tooltip:
        "Federal and state taxes are used to calculate tax incentives, and cash flow. The rates are defaulted as 21% and 7% respectively.",
    },
    {
      label: "Capacity Payments",
      accessor: "capacityPayments",
      tooltip:
        "Payments made to the BESS owner for committing capacity (to generate or store) when participating in demand response programs.",
    },
    { label: "Demand Response", accessor: "demandResponse", tooltip: "" },
  ];
  const handleClick = (value, makeSelection) => {
    const existingParameters = new Set(selectedParameters);
    if (!makeSelection) {
      existingParameters.delete(value);
      if (selectedForm === value) {
        setSelectedForm(undefined);
      }
    } else {
      existingParameters.add(value);
      setSelectedForm(value);
    }
    setSelectedParameters([...existingParameters]);
  };
  const handleSubmit = () => {
    let errors = JSON.parse(JSON.stringify(errorsInitialState));
    let foundError = false;
    selectedParameters.map((val) => {
      const currentState = { ...state[val] };
      const fields = formHelpers[val].fields;
      fields.map((feild) => {
        const value = currentState[feild.accessor];
        if (typeof value === "object") {
          if (value.value === "") {
            foundError = true;
            errors = {
              ...errors,
              [val]: {
                ...errors[val],
                haveError: true,
                [feild.accessor]: true,
              },
            };
          }
        } else {
          if (value === "") {
            foundError = true;
            errors = {
              ...errors,
              [val]: {
                ...errors[val],
                haveError: true,
                [feild.accessor]: true,
              },
            };
          }
        }
      });
    });
    setErrors(errors);
    if (!foundError) {
      const payload = {};
      selectedParameters.map((val) => {
        payload[val] = { ...state[val] };
      });
      const debt_percent = +state.projectDebt.debt_percent.value;

      const optimisedPayload = {
        project_length: +state.initialInvestment.project_length.value,
        initial_investment: +state.initialInvestment.initial_investment,
        debt_percent:
          state.projectDebt.debt_percent.selectedMeasureUnit === "%"
            ? debt_percent
            : (debt_percent / bessCost) * 100,
        debt_interest_rate: +state.projectDebt.debt_interest_rate,
        debt_term: +state.projectDebt.debt_term,
        property_tax_rate: +state.taxes.property_tax_rate,
        property_assessed_pct: +state.taxes.property_assessed_pct,
        fed_tax_rate: +state.taxes.fed_tax_rate,
        state_tax_rate: +state.taxes.state_tax_rate,
        insurance_rate: +state.taxes.insurance_rate,
      };
      console.log({ optimisedPayload });
      makeApiRequest({
        method: "post",
        urlPath: "Fancial_Analysis",
        body: { ...optimisedPayload },
      }).then(({ data, error }) => {
        if (error) {
          toast.error("Something went wrong");
        } else {
          setResults({ ...data.data });
          console.log({ data: { ...data.data } });
        }
      });
    } else {
      toast.error("Please fill all the fields");
    }
  };
  return (
    <div className={stylings[theme].financialAnalysis.masterStyle}>
      {!loaded ? (
        <div className="w-full h-[30rem] flex items-center justify-center">
          <Loader />
        </div>
      ) : (
        <>
          <span className=" w-full text-center text-[2rem] text-slate-400 font-bold pt-[1.5rem]">
            Financial Analysis
          </span>
          <div className=" w-full flex items-start justify-start">
            <div className=" w-[25%] pt-[1rem] ml-[2rem] shrink-0 flex flex-col items-center">
              <span
                className={stylings[theme].financialAnalysis.containerHeading}
              >
                Select Parameters
              </span>
              {parameters.map((val) => {
                return (
                  <div
                    className={
                      selectedParameters.includes(val.accessor)
                        ? stylings[theme].financialAnalysis.formOptions.selected
                        : stylings[theme].financialAnalysis.formOptions
                            .notSelected
                    }
                  >
                    <button
                      onClick={() => {
                        handleClick(val.accessor, true);
                      }}
                      className=" text-[1.2rem] py-[.4rem] flex-grow "
                    >
                      <label className="relative">
                        {val.label}
                        <ToolTip left={true} text={val.tooltip} />
                      </label>
                    </button>
                    {selectedParameters.includes(val.accessor) ? (
                      <>
                        <button
                          className=" pr-[0.2rem]"
                          onClick={() => {
                            if (selectedForm === val.accessor) {
                              setSelectedForm(undefined);
                            } else {
                              setSelectedForm(val.accessor);
                            }
                          }}
                        >
                          <SVGComponent
                            selector={
                              val.accessor === selectedForm
                                ? "eyeOpened"
                                : "eyeClosed"
                            }
                            width={"w-[1.5rem]"}
                            color={
                              val.accessor === selectedForm
                                ? stylings[theme].financialAnalysis.svgEyeColor
                                    .selected
                                : stylings[theme].financialAnalysis.svgEyeColor
                                    .notSelected
                            }
                          />
                        </button>
                        <button
                          className=" pr-[0.2rem]"
                          onClick={() => {
                            handleClick(val.accessor, false);
                          }}
                        >
                          <SVGComponent
                            selector={"boldCross"}
                            width={"w-[1.5rem]"}
                            color={
                              stylings[theme].financialAnalysis
                                .svgEyeCrossButton
                            }
                          />
                        </button>
                      </>
                    ) : (
                      <></>
                    )}
                  </div>
                );
              })}
              <button
                onClick={() => {
                  handleSubmit();
                }}
                className={stylings[theme].financialAnalysis.calculateButton}
              >
                Calculate
              </button>
            </div>
            <Results
              results={results}
              renderResultsHelper={renderResultsHelper}
            />
            {selectedForm ? (
              <RenderForm
                bessPower={bessPower}
                errors={errors[selectedForm]}
                val={selectedForm}
                formHelper={formHelpers[selectedForm]}
                state={state}
                setState={setState}
              />
            ) : (
              <div className=" w-[30%] h-[100%] flex flex-col items-center justify-center">
                <SVGComponent
                  selector="select"
                  width="w-[5rem]"
                  color="#94A3B8"
                />
                <span className=" text-[1.5rem] text-slate-400 font-semibold">
                  Please Select a Parameter
                </span>
              </div>
            )}
          </div>
          <div className=" w-full mt-[4rem] h-fit flex items-start justify-evenly"></div>
        </>
      )}
    </div>
  );
}
