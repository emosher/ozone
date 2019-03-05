import "reflect-metadata";

import { PreferenceAPI, PreferenceCreateRequest, PreferenceUpdateRequest } from "../../src/api/clients/PreferenceAPI";

import { NodeGateway } from "./node-gateway";
import { PREFERENCES } from "../unit/data";

describe("Preference API", () => {
    let gateway: NodeGateway;
    let preferenceApi: PreferenceAPI;
    let newSetting: PreferenceCreateRequest;
    let newPreference: PreferenceCreateRequest;

    beforeAll(async () => {
        gateway = new NodeGateway();
        preferenceApi = new PreferenceAPI(gateway);

        newSetting = {
          id: 6,
          namespace: "owf.admin.WidgetEditCopy",
          path: "newSetting",
          value: "someValue2",
          user: {userId: "testAdmin1"}
        }

        newPreference = {
          id: 7,
          namespace: "newField",
          path: "newSetting3",
          value: "someOtherValue",
          user: {userId: ""}
        }

        await gateway.login("testAdmin1", "password");
        expect(gateway.isAuthenticated).toEqual(true);
    });

    test("getPreferences - GET /prefs/preference/", async () => {
        let response;
        try {
            response = await preferenceApi.getPreferences();
        }
        catch (ex) {
            console.dir(ex.errors);
            return fail();
        }

        expect(response.status).toEqual(200);
        expect(response.data).toEqual({
            success: true,
            results: 5,
            rows: PREFERENCES
        });
    });

    test("getPreferences by namespace - GET /prefs/preference/:namespace/", async () => {
        let response;
        try {
            response = await preferenceApi.getPreferences("owf.admin.WidgetEditCopy");
        }
        catch (ex) {
            console.dir(ex.errors);
            return fail();
        }

        expect(response.status).toEqual(200);

        expect(response.data).toEqual({
            success: true,
            results: 1,
            rows: [PREFERENCES[1]]
        });
    });

    test("getPreference - GET /prefs/preference/:namespace/:path/", async () => {
        let response;
        try {
            response = await preferenceApi.getPreference("owf.admin.WidgetEditCopy", "guid_to_launch");
        }
        catch (ex) {
            console.dir(ex.errors);
            return fail();
        }

        expect(response.status).toEqual(200);
        console.dir(response.data, {depth: null});
        expect(response.data).toEqual(PREFERENCES[1]);
    });

    test("getServerResources - GET /prefs/server/resources/", async () => {
        const response = await preferenceApi.getServerResources();

        expect(response.status).toEqual(200);
        expect(response.data).toEqual({
            serverVersion: "7.17.2-0"
        });
    });

    test("createPreference - POST /prefs/preference/:namespace/:path/", async () => {
        let createSettingResponse;
        try {
          createSettingResponse = await preferenceApi.createPreference(newSetting);
        }
        catch(e) {
          console.dir(e.errors);
          return fail();
        }

        expect(createSettingResponse.status).toEqual(200);
        console.dir(createSettingResponse.data, {depth: null});
        newSetting.id = createSettingResponse.data.id;

        expect(createSettingResponse.data).toEqual(newSetting);



        let getNewSettingResponse;
        try {
          getNewSettingResponse = await preferenceApi.getPreference(newSetting.namespace, newSetting.path);
        }
        catch(e) {
          console.dir(e.errors);
          return fail();
        }
        expect(getNewSettingResponse.status).toEqual(200);
        console.dir(getNewSettingResponse.data);

        expect(getNewSettingResponse.data).toEqual(newSetting);



        console.dir(newSetting);


        let deleteSettingResponse;
        try {
          deleteSettingResponse  = await preferenceApi.deletePreference(newSetting);
        }
        catch(e) {
          console.dir(e.errors);
          return fail();
        }

        expect(deleteSettingResponse.status).toEqual(200);
        console.dir(deleteSettingResponse.data);

        expect(deleteSettingResponse.data).toEqual(newSetting);



        let getBaseResponse;
        try {
           getBaseResponse = await preferenceApi.getPreferences();
        }
        catch(e) {
          console.dir(e.errors);
          return fail();
        }
        expect(getBaseResponse.status).toEqual(200);
        console.dir(getBaseResponse.data);

        expect(getBaseResponse.data).toEqual({
          success: true,
          results: 5,
          rows: PREFERENCES
        });


        // const prefResponse = await preferenceApi.createPreference(newPreference);
        // expect(prefResponse.data).toEqual(newPreference);
        //
        // const getNewPreferenceResponse = await preferenceApi.getPreference(newPreference.namespace, newPreference.path);
        // expect(getNewPreferenceResponse.status).toEqual(200);
        // expect(getNewPreferenceResponse.data).toEqual(newPreference);
        //
        // let deletePrefResponse = await preferenceApi.deletePreference(newPreference);
        // expect(deletePrefResponse.status).toEqual(200);
        // expect(deletePrefResponse.data).toEqual(newPreference);
        //
        // const getBaseResponse2 = await preferenceApi.getPreferences();
        // expect(getBaseResponse2.status).toEqual(200);
        // expect(getBaseResponse2.data).toEqual({
        //   success: true,
        //   results: 5,
        //   rows: PREFERENCES
        // });

    });
});
