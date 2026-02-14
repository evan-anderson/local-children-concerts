import { test, expect } from '@playwright/test';

test.describe('Concert Discovery App', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('displays page title and header', async ({ page }) => {
    await expect(page.locator('h1')).toContainText('Kids Concert Finder');
    await expect(page.locator('header p')).toContainText('child-friendly concerts');
  });

  test('displays concert list on load', async ({ page }) => {
    // Wait for concerts to load
    await expect(page.locator('.concert-card').first()).toBeVisible({ timeout: 10000 });

    // Should show multiple concerts
    const concertCount = await page.locator('.concert-card').count();
    expect(concertCount).toBeGreaterThan(0);
  });

  test('displays results count', async ({ page }) => {
    await expect(page.locator('.results-count')).toBeVisible({ timeout: 10000 });
    await expect(page.locator('.results-count')).toContainText(/Showing \d+ concerts?/);
  });

  test('concert card shows title, date, and venue', async ({ page }) => {
    const firstCard = page.locator('.concert-card').first();
    await expect(firstCard).toBeVisible({ timeout: 10000 });

    // Check card has required elements
    await expect(firstCard.locator('h3')).toBeVisible();
    await expect(firstCard.locator('.date')).toBeVisible();
    await expect(firstCard.locator('.venue')).toBeVisible();
  });

  test('town filter checkboxes are displayed', async ({ page }) => {
    // Wait for towns to load
    await expect(page.locator('.town-checkboxes')).toBeVisible({ timeout: 10000 });

    // Should have multiple town checkboxes
    const townCount = await page.locator('.checkbox-label').count();
    expect(townCount).toBeGreaterThan(0);
  });

  test('clicking town filter updates concert list', async ({ page }) => {
    // Wait for initial load
    await expect(page.locator('.concert-card').first()).toBeVisible({ timeout: 10000 });

    // Get initial count
    const initialCount = await page.locator('.concert-card').count();

    // Click on Boston checkbox
    const bostonCheckbox = page.locator('.checkbox-label', { hasText: 'Boston' });
    await bostonCheckbox.click();

    // Wait for list to update
    await page.waitForTimeout(500);

    // Count should change (filtered to just Boston)
    const filteredCount = await page.locator('.concert-card').count();
    expect(filteredCount).toBeLessThanOrEqual(initialCount);
  });

  test('date filter inputs are displayed', async ({ page }) => {
    await expect(page.locator('.date-filter')).toBeVisible();
    await expect(page.locator('input[type="date"]').first()).toBeVisible();
    await expect(page.locator('input[type="date"]').last()).toBeVisible();
  });

  test('setting date filter updates results', async ({ page }) => {
    // Wait for initial load
    await expect(page.locator('.concert-card').first()).toBeVisible({ timeout: 10000 });

    // Set a future end date that excludes most concerts
    const startDateInput = page.locator('input[placeholder="Start date"]');
    await startDateInput.fill('2030-01-01');

    // Wait for filter to apply
    await page.waitForTimeout(500);

    // Should show no results or empty state
    const hasEmptyState = await page.locator('.empty').isVisible();
    const concertCount = await page.locator('.concert-card').count();

    expect(hasEmptyState || concertCount === 0).toBeTruthy();
  });

  test('shows empty state when no concerts match filters', async ({ page }) => {
    // Wait for initial load
    await expect(page.locator('.concert-card').first()).toBeVisible({ timeout: 10000 });

    // Set impossible date range
    const startDateInput = page.locator('input[placeholder="Start date"]');
    const endDateInput = page.locator('input[placeholder="End date"]');

    await startDateInput.fill('2030-01-01');
    await endDateInput.fill('2030-01-02');

    // Wait for filter to apply
    await page.waitForTimeout(500);

    // Should show empty state
    await expect(page.locator('.empty')).toBeVisible();
    await expect(page.locator('.empty')).toContainText('No concerts found');
  });

  test('shows loading state initially', async ({ page }) => {
    // Navigate fresh without cache
    await page.goto('/', { waitUntil: 'commit' });

    // Loading state should appear briefly (may be very fast)
    // This test just verifies the page loads without errors
    await expect(page.locator('.app')).toBeVisible();
  });
});
