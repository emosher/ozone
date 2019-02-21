import * as React from "react";
import { Form, Formik, FormikActions, FormikProps } from "formik";

import { lazyInject } from "../../inject";
import { PremadeLayouts } from "./PremadeLayouts";
import { DashboardSelect } from "./DashboardSelect";

import { FormError, SubmitButton, TextField } from "../form";
import { DashboardUpdateRequest } from "../../api/models/dashboard-dto";
import { DashboardAPI } from "../../api";
import { Radio, RadioGroup } from "@blueprintjs/core";

import * as styles from "./CreateDashboardStyles.scss";

import * as Util from "../util";

import uuid from "uuid/v4";
const myUuid = uuid();

export interface CreateDashboardFormProps {
    onSubmit: () => void;
}

export interface State {
    showPremades: boolean;
    showCopy: boolean;
    createNew: boolean;
    hidden: boolean;
    value: string;
}

export class CreateDashboardForm extends React.Component<CreateDashboardFormProps, State> {
    @lazyInject(DashboardAPI)
    private dashboardAPI: DashboardAPI;

    private handleRadioChange = Util.handleStringChange((value) => this.setState({ value }));

    constructor(props: any) {
        super(props);
        this.state = {
            showPremades: false,
            showCopy: false,
            createNew: false,
            hidden: false,
            value: ""
        };
    }

    render() {
        return (
            <Formik
                initialValues={{
                    name: "",
                    guid: myUuid,
                    iconImageUrl: "https://cdn.onlinewebfonts.com/svg/img_301147.png",
                    description: ""
                }}
                // validationSchema={NewDashboardRequestSchema}
                onSubmit={async (values: DashboardUpdateRequest, actions: FormikActions<DashboardUpdateRequest>) => {
                    const isSuccess = await this.dashboardAPI.createDashboard(values);
                    if (isSuccess) {
                        this.props.onSubmit();
                        actions.setStatus(null);
                    } else {
                        actions.setStatus({ error: "An unexpected error has occurred" });
                    }
                }}
            >
                {(formik: FormikProps<DashboardUpdateRequest>) => (
                    <Form>
                        {formik.status && formik.status.error && <FormError message={formik.status.error} />}

                        <div className={styles.ParentStyles}>
                            <div className={styles.IconStyles}>
                                <img width="60px" src={formik.values.iconImageUrl} />
                            </div>
                            <div className={styles.FieldStyles}>
                                <TextField name="name" label="Title" labelInfo="(required)" />
                                {this.state.hidden && <TextField name="guid" label="guid" />}
                                <TextField name="iconImageUrl" label="Icon Url" />
                                <TextField name="description" label="Description" />
                            </div>
                        </div>
                        <RadioGroup onChange={this.handleRadioChange} selectedValue={this.state.value}>
                            <Radio label="Choose a premade layout" value="premade" />
                            {this.state.value === "premade" && <PremadeLayouts onChange={this.handleRadioChange} />}
                            <Radio label="Copy the layout of an existing page" value="copy" />
                            {this.state.value === "copy" && <DashboardSelect />}
                            <Radio label="Create a new layout" value="new" />
                        </RadioGroup>

                        <SubmitButton />
                    </Form>
                )}
            </Formik>
        );
    }
}