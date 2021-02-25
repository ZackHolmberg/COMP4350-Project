// https://docs.cypress.io/api/introduction/api.html

describe('Sends a transaction', () => {
    context('1080p resolution', () => {
      beforeEach(() => {
        // run these tests as if in a desktop
        cy.viewport(1920, 1080)
        cy.visit('http://localhost:8080/')
        cy.get('#username').type('Username') 
        cy.get('#password').type('Password') 
        cy.get('#button').click()
      })
 
      it('Successfully navigates to transaction page', () => {
        cy.get('#transaction-button').click()
        cy.url().should('eq', 'http://localhost:8080/transaction')     
      })

      it('Sends new transaction', () => {
        cy.get('#transaction-button').click()
        cy.get('#contact-input').type('Email') 
        cy.get('#amount-input').type('0')
        cy.get('#transaction-send').click()   
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