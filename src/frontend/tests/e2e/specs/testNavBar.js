describe("Checks nav bar", () => {
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

    it("Nav bar icons are visible", () => {
      cy.url().should("eq", "http://localhost:8080/home");
      cy.get("#nav-logo").should("be.visible");
      cy.get("#nav-account").should("be.visible");
      cy.get("#nav-logout").should("be.visible");
    });

    it("Account icon navigates to account page", () => {
      cy.get("#nav-account").click();
      cy.url().should("eq", "http://localhost:8080/account");
    });
  });
});
