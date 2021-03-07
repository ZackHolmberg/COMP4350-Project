describe("Checks account page", () => {
  context("1080p resolution", () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      cy.viewport(1920, 1080);
      cy.visit("http://localhost:8080/");
      cy.get("#umnetId").type("umnetId");
      cy.get("#password").type("Password");
      cy.intercept("POST", "/users/login", { fixture: "success.json" }).as(
        "userLogin"
      );
      cy.intercept("POST", "/wallet/amount", {
        fixture: "walletAmountEmpty.json",
      }).as("getWalletAmount");
      cy.get("#button").click();
      cy.wait(["@userLogin"]);
      cy.wait(["@getWalletAmount"]);
      cy.get("#nav-account").click();
    });

    it("Account details are visible", () => {
      cy.url().should("eq", "http://localhost:8080/account");
      cy.get("#account-cancel").should("be.visible");
      cy.get("#account-edit").should("be.visible");
      cy.get("#account-first-name").should("be.visible");
      cy.get("#account-last-name").should("be.visible");
      cy.get("#account-umnetId").should("be.visible");
      cy.get("#account-password").should("be.visible");
    });

    it("Cancels view account", () => {
      cy.get("#account-cancel").click();
      cy.url().should("eq", "http://localhost:8080/home");
    });
  });
});
