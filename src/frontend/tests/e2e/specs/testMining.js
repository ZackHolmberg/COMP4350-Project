describe("Mining Component", () => {
  context("1080p resolution", () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      cy.viewport(1920, 1080);
      cy.visit("http://localhost:8080/");
      cy.get("#umnetId").type("umnetId");
      cy.get("#password").type("Password");
      cy.intercept("POST", "/users/login", { fixture: "loginSuccess.json" }).as(
        "userLogin"
      );
      cy.intercept("POST", "/wallet/amount", {
        fixture: "walletAmountEmpty.json",
      }).as("getWalletAmount");
      cy.get("#login-button").click();
      cy.wait(["@userLogin"]);
      cy.wait(["@getWalletAmount"]);
    });

    it("Validates that the mining component is visible and value is as expected", () => {
      cy.url().should("eq", "http://localhost:8080/home");
      mining = cy.get('[id="mining"]');
      mining.should("be.visible");
      mining.contains("Mining Off");
      mining.click();
      mining.contains("Mining On");
    });
  });
});
