import unittest
from unittest.mock import patch, Mock
import stockfinderv2


class TestStockFinder(unittest.TestCase):

    @patch('stockfinderv2.scrape_symbols')
    @patch('stockfinderv2.get_factors')
    @patch('csv.writer')
    def test_fetchStocksByMarketv2(self, mock_writer, mock_get_factors, mock_scrape_symbols):
        mock_scrape_symbols.return_value = ['AAPL', 'GOOGL']
        mock_get_factors.return_value = (1, 1, 1)

        self.assertEqual(stockfinderv2.fetchStocksByMarketv2('NASDAQ'), ['AAPL', 'GOOGL'])

    def test_get_factors(self):
        with patch('yfinance.Ticker') as mock_ticker:
            mock_ticker().info = {'trailingPE': 1, 'beta': 1, 'trailingEps': 1}
            self.assertEqual(stockfinderv2.get_factors('AAPL'), (1, 1, 1))

    @patch('stockfinderv2.get_factors')
    def test_select_best_stocks(self, mock_get_factors):
        mock_get_factors.return_value = (1, 1, 1)
        self.assertEqual(stockfinderv2.select_best_stocks(['AAPL', 'GOOGL'], 1), ['AAPL'])

    @patch('requests.get')
    def test_scrape_symbols(self, mock_get):
        mock_get.return_value = Mock()
        mock_get.return_value.text = '<table class="quotes"><tr><td>AAPL</td></tr></table>'
        apple_array = ['AAPL'] * 26
        self.assertEqual(stockfinderv2.scrape_symbols('NASDAQ'), apple_array)

    @patch('stockfinderv2.fetchStocksByMarketv2')
    @patch('stockfinderv2.select_best_stocks')
    def test_fetchStocksByMarketAndReduceSizeOfList(self, mock_select_best_stocks, mock_fetchStocksByMarketv2):
        mock_fetchStocksByMarketv2.return_value = ['AAPL', 'GOOGL']
        mock_select_best_stocks.return_value = ['AAPL']
        self.assertEqual(stockfinderv2.fetchStocksByMarketAndReduceSizeOfList('NASDAQ', 1), ['AAPL'])

    @patch('stockfinderv2.scrape_symbols')
    @patch('csv.writer')
    def test_fetchStocksByMarket(self, mock_writer, mock_scrape_symbols):
        mock_scrape_symbols.return_value = ['AAPL', 'GOOGL']
        self.assertEqual(stockfinderv2.fetchStocksByMarket('NASDAQ'), ['AAPL', 'GOOGL'])


if __name__ == '__main__':
    unittest.main()
