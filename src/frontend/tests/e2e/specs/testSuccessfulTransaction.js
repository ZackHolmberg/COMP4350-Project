describe("Sends a transaction successfully", () => {
  context("1080p resolution", () => {
    beforeEach(() => {
      // run these tests as if in a desktop
      cy.viewport(1920, 1080);
      cy.visit("http://localhost:8080/");
      cy.get("#create-account-link").click();
      cy.get("#umnetId").type("umnetId");
      cy.get("#password").type("Password");
      cy.get("#password2").type("Password");
      cy.get("#first-name").type("firstName");
      cy.get("#last-name").type("lastName");

      cy.intercept("POST", "/users/create", { fixture: "success.json" }).as(
        "createAccount"
      );
      cy.intercept("POST", "/users/login", { fixture: "loginSuccess.json" }).as(
        "userLogin"
      );
      cy.intercept("POST", "/wallet/amount", {
        fixture: "walletAmountEmpty.json",
      }).as("getWalletAmount");

      cy.get("#create-account-button").click();
      cy.wait(["@createAccount"]);
      cy.wait(["@userLogin"]);
      cy.wait(["@getWalletAmount"]);
      cy.url().should("eq", "http://localhost:8080/home");
    });

    it("Successfully navigates to transaction page", () => {
      cy.get("#transaction-button").click();
      cy.url().should("eq", "http://localhost:8080/transaction");
    });

    it("Successfully sends new transaction", () => {
      cy.get("#transaction-button").click();
      cy.get("#contact-input").type("umnetId");
      cy.get("#amount-input").type("2");

      cy.intercept("POST", "/transactions/create", {
        fixture: "transaction.json",
      }).as("transactionCreate");
      cy.get("#transaction-send").click();
      cy.wait(["@transactionCreate"]);
      transaction = cy.get('[class="v-toast__text"]');
      transaction.should("be.visible");
      transaction.contains("Transaction sent successfully!");
      cy.get("#walletAmount");

      cy.url().should("eq", "http://localhost:8080/home");
    });
  });
});
