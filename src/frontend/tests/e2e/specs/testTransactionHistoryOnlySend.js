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
        fixture: "transactionHistoryOnlySend.json",
      }).as("getTransactionHistory");
      cy.get("#login-button").click();
      cy.wait(["@userLogin"]);
      cy.wait(["@getTransactionHistory"]);
      cy.wait(["@getWalletAmount"]);
    });

    it("Validates that the transaction history toast does not pop up", () => {
      cy.url().should("eq", "http://localhost:8080/home");
      loginToast = cy.get('[class="v-toast__text"]');
      loginToast.should("be.visible");
      loginToast.contains("Login successful!");
      newTransactionToast = cy.get('[class="v-toast__text"]');
      newTransactionToast.should("not.exist");
    });
  });
});
