import { test, expect } from '@playwright/test';

test.describe('PharmaBot Application', () => {
  test('page loads successfully', async ({ page }) => {
    await page.goto('/');
    
    // Vérifie que le titre existe
    await expect(page.getByRole('heading', { name: 'PharmaBot' })).toBeVisible();
    
    // Vérifie le sous-titre
    await expect(page.getByText('Assistant professionnel - Vidal & Meddispar')).toBeVisible();
  });

  test('displays welcome message', async ({ page }) => {
    await page.goto('/');
    
    // Vérifie le message de bienvenue
    await expect(page.getByText('Assistant pour Pharmaciens')).toBeVisible();
    await expect(page.getByText('Outil professionnel d\'aide à la recherche')).toBeVisible();
  });

  test('displays example questions', async ({ page }) => {
    await page.goto('/');
    
    // Vérifie les questions d'exemple
    await expect(page.getByText('Quelles sont les indications du paracétamol ?')).toBeVisible();
    await expect(page.getByText('Interactions médicamenteuses de l\'aspirine')).toBeVisible();
  });

  test('input field is present and functional', async ({ page }) => {
    await page.goto('/');
    
    const input = page.getByPlaceholder('Posez votre question pharmaceutique...');
    await expect(input).toBeVisible();
    await expect(input).toBeEnabled();
    
    // Test saisie
    await input.fill('Test question');
    await expect(input).toHaveValue('Test question');
  });

  test('send button is present', async ({ page }) => {
    await page.goto('/');
    
    const sendButton = page.getByRole('button').filter({ has: page.locator('svg') }).last();
    await expect(sendButton).toBeVisible();
  });

  test('displays legal disclaimer', async ({ page }) => {
    await page.goto('/');
    
    // Vérifie l'avertissement légal
    await expect(page.getByText(/Avertissement Légal/)).toBeVisible();
    await expect(page.getByText(/outil d'aide à la décision/)).toBeVisible();
  });

  test('can send a message and receive response', async ({ page }) => {
    await page.goto('/');
    
    // Remplir et envoyer un message
    const input = page.getByPlaceholder('Posez votre question pharmaceutique...');
    await input.fill('Quelles sont les indications du paracétamol?');
    
    const sendButton = page.getByRole('button').filter({ has: page.locator('svg') }).last();
    await sendButton.click();
    
    // Attendre la réponse
    await page.waitForTimeout(5000); // Attend que l'API réponde
    
    // Vérifie que le message utilisateur apparaît
    await expect(page.getByText('Quelles sont les indications du paracétamol?')).toBeVisible();
    
    // Vérifie qu'une réponse est reçue (contient du texte)
    const messages = page.locator('[class*="rounded-lg"]');
    await expect(messages.first()).toBeVisible({ timeout: 10000 }); // Au moins un message visible
  });

  test('displays sources when available', async ({ page }) => {
    await page.goto('/');
    
    const input = page.getByPlaceholder('Posez votre question pharmaceutique...');
    await input.fill('Paracétamol posologie');
    
    const sendButton = page.getByRole('button').filter({ has: page.locator('svg') }).last();
    await sendButton.click();
    
    // Attendre la réponse avec sources
    await page.waitForTimeout(6000);
    
    // Vérifie que les sources apparaissent
    await expect(page.getByText('Sources :')).toBeVisible({ timeout: 10000 });
  });

  test('navigation to search page works', async ({ page }) => {
    await page.goto('/');
    
    // Cliquer sur le bouton Recherche
    await page.getByRole('button', { name: /Recherche/ }).click();
    
    // Vérifie qu'on est sur la page de recherche
    await expect(page.getByRole('heading', { name: 'Recherche dans la base' })).toBeVisible();
  });

  test('search page functionality', async ({ page }) => {
    await page.goto('/search');
    
    // Vérifie les éléments de la page
    await expect(page.getByPlaceholder('Rechercher un médicament, une maladie...')).toBeVisible();
    await expect(page.getByRole('button', { name: /Rechercher/ })).toBeVisible();
    
    // Vérifie les filtres de source
    await expect(page.getByRole('button', { name: 'Toutes les sources' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Vidal' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Meddispar' })).toBeVisible();
  });

  test('can perform search', async ({ page }) => {
    await page.goto('/search');
    
    const searchInput = page.getByPlaceholder('Rechercher un médicament, une maladie...');
    await searchInput.fill('paracétamol');
    
    const searchButton = page.getByRole('button', { name: /Rechercher/ });
    await searchButton.click();
    
    // Attendre les résultats
    await page.waitForTimeout(3000);
    
    // Vérifie qu'il y a des résultats
    await expect(page.getByText(/résultat/)).toBeVisible({ timeout: 10000 });
  });

  test('clear chat button appears after sending message', async ({ page }) => {
    await page.goto('/');
    
    // Envoyer un message
    const input = page.getByPlaceholder('Posez votre question pharmaceutique...');
    await input.fill('Test');
    await page.getByRole('button').filter({ has: page.locator('svg') }).last().click();
    
    await page.waitForTimeout(3000);
    
    // Vérifie que le bouton Effacer apparaît
    await expect(page.getByRole('button', { name: /Effacer/ })).toBeVisible({ timeout: 5000 });
  });
});
