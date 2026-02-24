-- Run this script in the Supabase SQL Editor to update the database schema
-- It adds the new columns for the Linear Markup rules and Discount logic.

ALTER TABLE pricing_history 
ADD COLUMN valor_com_comissao FLOAT,
ADD COLUMN valor_com_margem FLOAT,
ADD COLUMN valor_venda_cheio FLOAT,
ADD COLUMN valor_minimo_venda FLOAT,
ADD COLUMN desconto_concedido_perc FLOAT DEFAULT 0.0,
ADD COLUMN valor_com_desconto FLOAT;
