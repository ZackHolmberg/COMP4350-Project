describe('Fails to send a transaction', () => {
    context('1080p resolution', () => {
      beforeEach(() => {
        // run these tests as if in a desktop
        cy.viewport(1920, 1080)
        cy.visit('http://localhost:8080/')
        cy.get('#username').type('Username') 
        cy.get('#password').type('Password') 
        cy.intercept('POST', '/wallet/create', {fixture: 'success.json'}).as('createWallet')
        cy.intercept('POST', '/wallet/amount', {fixture: 'walletAmountEmpty.json'}).as('getWalletAmount')
        cy.get('#button').click()
        cy.wait(['@createWallet'])
        cy.wait(['@getWalletAmount'])
      })

      it('Fails to send transaction due to insufficient funds', () => {
        cy.get('#transaction-button').click()
        cy.get('#contact-input').type('Email') 
        cy.get('#amount-input').type('0')

        cy.intercept('POST', '/transactions/create', {
          statusCode: 400, 
          body: { err: "Unable to Verify the Wallet Amount" }
        }).as('transactionCreate')
        cy.get('#transaction-send').click()   
        cy.wait(['@transactionCreate'])
        transaction = cy.get('[class="v-toast__text"]')
        transaction.should('be.visible')    
        transaction.contains('Unable to Verify the Wallet Amount')    
        cy.url().should('eq', 'http://localhost:8080/home') 
      })

      it('Cancels new transaction', () => {
        cy.get('#transaction-button').click()
        cy.get('#contact-input').type('Email') 
        cy.get('#amount-input').type('0')
        cy.get('#transaction-cancel').click() 
        cy.url().should('eq', 'http://localhost:8080/home') 
      })
    })
  })

  