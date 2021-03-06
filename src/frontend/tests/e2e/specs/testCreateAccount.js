describe("After loading the app", () => {
  context("1080p resolution", () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      cy.viewport(1920, 1080);
      cy.visit("http://localhost:8080/");
    });

    it("Successfully navigates to create account page, enters information, and logs into app", () => {
      cy.get("#create-account-link").click();
      cy.get("#umnetId").type("umnetId");
      cy.get("#password").type("Password");
      cy.get("#password2").type("Password");
      cy.get("#first-name").type("firstName");
      cy.get("#last-name").type("lastName");

      cy.intercept("POST", "/users/create", { fixture: "success.json" }).as(
        "createAccount"
      );
      cy.intercept("POST", "/users/login", { fixture: "success.json" }).as(
        "userLogin"
      );
      cy.intercept("POST", "/wallet/create", { fixture: "success.json" }).as(
        "createWallet"
      );
      cy.intercept("POST", "/wallet/amount", {
        fixture: "walletAmountEmpty.json",
      }).as("getWalletAmount");

      cy.get("#create-account-button").click();
      cy.wait(["@createAccount"]);
      cy.wait(["@createWallet"]);
      cy.wait(["@userLogin"]);
      cy.wait(["@getWalletAmount"]);
      cy.url().should("eq", "http://localhost:8080/home");
    });
  });
});
