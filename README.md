# Bellamoosh ERP

Custom Frappe app for **Bellamoosh Lifestyle LLP** — Fabric Export Operations

## Features

- **Purchase Order Management** with Chart No and Branch tracking
- **Goods Inward Receipt (GRN)** with Quality Checking
- **Taka Checking** with Wastage Formula Support
- **Bale & Roll Management** for fabric organization
- **Carton Packing** with weight tracking
- **Sample Entry** for vendor samples
- **Custom Reports** for supply chain visibility
- **Multi-branch Support** (Headoffice, Surat, Bhiwandi)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/bellamoosh_erp.git
   ```

2. In your Frappe Cloud site, go to Apps → Install App

3. Click "Add from GitHub" and select this repo

4. Click Install

The app will automatically install all custom fields, DocTypes, and reports.

## Custom DocTypes

- **Taka Checking** — Quality checking with automatic wastage categorization
- **Roll** — Fabric roll creation from cutting details
- **Carton** — Carton packing from rolls
- **Sample Entry** — Sample tracking from vendors

## Custom Fields

Adds fields to Purchase Order, Purchase Receipt, Stock Entry, Delivery Note, and Item.

## Reports

- **Item Flow Report** — Tracks fabric from PO to delivery
- **Cutting and Packing Report** — Wastage and packing analysis
- **Post Delivery Summary** — Delivery metrics and loss percentage

## Author

Bellamoosh Lifestyle LLP

## License

MIT
