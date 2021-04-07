describe("Transaction History Component", () => {
  context("1080p resolution", () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      // browser with a 1080p monitor
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
      cy.intercept("GET", "/wallet/history/umnetId", {
        fixture: "transactionHistory.json",
      }).as("getTransactionHistory");
      cy.get("#login-button").click();
      cy.wait(["@userLogin"]);
      cy.wait(["@getTransactionHistory"]);
      cy.wait(["@getWalletAmount"]);
    });

    it("Validates that the transaction history component is visible when clicked and looks as expected", () => {
      cy.url().should("eq", "http://localhost:8080/home");
      button = cy.get('[id="transaction-history-button"]');
      button.should("be.visible");
      button.click();
      content = cy.get('[id="content"]');
      content.should("be.visible");
    });

    it("Navigates back to the home screen when the back button is pressed", () => {
      cy.url().should("eq", "http://localhost:8080/home");
      button = cy.get('[id="transaction-history-button"]');
      button.should("be.visible");
      button.click();
      content = cy.get('[id="content"]');
      content.should("be.visible");
      cy.url().should("eq", "http://localhost:8080/transactionHistory");
      button = cy.get('[id="transaction-history-back-button"]');
      button.should("be.visible");
      button.click();
      cy.url().should("eq", "http://localhost:8080/home");
    });
  });
});
