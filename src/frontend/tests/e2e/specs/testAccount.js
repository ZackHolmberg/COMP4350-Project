describe('Checks account page', () => {
    context('1080p resolution', () => {
      beforeEach(() => {
        // run these tests as if in a desktop
        cy.viewport(1920, 1080)
        cy.visit('http://localhost:8080/')
        cy.get('#username').type('Username') 
        cy.get('#password').type('Password') 
        cy.get('#button').click()
        cy.get('#nav-account').click()  
      })
 
      it('Account details are visible', () => {   
        cy.url().should('eq', 'http://localhost:8080/account')  
        cy.get('#account-cancel').should('be.visible') 
        cy.get('#account-edit').should('be.visible')
        cy.get('#account-name').should('be.visible')
        cy.get('#account-email').should('be.visible')
        cy.get('#account-umnetId').should('be.visible')   
        cy.get('#account-password').should('be.visible') 
      })

      it('Cancels view account', () => {
        cy.get('#account-cancel').click() 
        cy.url().should('eq', 'http://localhost:8080/home') 
      })
    })
  })