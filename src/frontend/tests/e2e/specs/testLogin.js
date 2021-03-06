describe("After loading the app", () => {
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
    });

    it("Successfully logs into the app and navigates to home page", () => {
      cy.url().should("eq", "http://localhost:8080/home");
    });
  });
});
