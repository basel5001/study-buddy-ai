import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the study buddy heading', () => {
  render(<App />);
  expect(screen.getByText(/study buddy/i)).toBeInTheDocument();
  expect(screen.getByText(/ai-powered quiz generator/i)).toBeInTheDocument();
});
