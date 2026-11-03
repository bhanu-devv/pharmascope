// Power Query M template for Power BI Desktop; edit the CSV path for each table.
// For purchase_orders, replace the path with your local extracted folder.
let
    Source = Csv.Document(File.Contents("C:\path\to\pharma_supply_chain_portfolio\data\purchase_orders.csv"),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    PromotedHeaders = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(PromotedHeaders,{
      {"po_id",Int64.Type},{"supplier_id",Int64.Type},{"material_id",Int64.Type},
      {"order_date",type date},{"promised_date",type date},{"received_date",type date},
      {"quantity",Int64.Type},{"unit_price",type number},{"actual_spend",type number},
      {"standard_spend",type number},{"price_variance",type number},
      {"late_flag",Int64.Type},{"invoice_amount",type number},{"invoice_variance",type number},
      {"invoice_exception",Int64.Type},{"year",Int64.Type},{"month",type text}
    })
in Typed
