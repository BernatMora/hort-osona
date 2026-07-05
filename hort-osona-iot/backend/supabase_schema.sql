-- =============================================================
-- Hort Osona IoT - Schema Supabase
-- =============================================================
-- Executar a la consola SQL de Supabase (https://app.supabase.com)
-- 
-- Crea 2 taules:
-- 1. mesures: historic de lectures dels sensors
-- 2. consells_ia: ultim consell generat per Ollama
--
-- Activa tambe el Realtime per tal que la web rebi les dades
-- en temps real (automatic quan fas INSERT).
-- =============================================================


-- ──────────── Taula 1: mesures ────────────
CREATE TABLE IF NOT EXISTS public.mesures (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    node_id TEXT NOT NULL DEFAULT 'hort-osona-01',
    temperatura_c REAL,
    humitat_amb_pct REAL,
    pressio_hpa REAL,
    humitat_sol_pct INTEGER,
    bateria_v REAL,
    rssi_dbm REAL,
    snr_db REAL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index per a consultes per data
CREATE INDEX IF NOT EXISTS idx_mesures_ts ON public.mesures (ts DESC);
CREATE INDEX IF NOT EXISTS idx_mesures_node_ts ON public.mesures (node_id, ts DESC);

-- Activar Realtime (important per la web)
ALTER PUBLICATION supabase_realtime ADD TABLE public.mesures;


-- ──────────── Taula 2: consells_ia ────────────
CREATE TABLE IF NOT EXISTS public.consells_ia (
    id BIGSERIAL PRIMARY KEY,
    ts TIMESTAMPTZ NOT NULL DEFAULT now(),
    consell TEXT NOT NULL,
    font TEXT DEFAULT 'ollama',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER PUBLICATION supabase_realtime ADD TABLE public.consells_ia;


-- ──────────── Row Level Security (RLS) ────────────
-- IMPORTANT: Aquestes taules son publiques (llegir) pero nomes
-- el backend pot escriure. Activa RLS i configura les policies.

ALTER TABLE public.mesures ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.consells_ia ENABLE ROW LEVEL SECURITY;

-- Policy: tothom pot LLEGIR (per la web publica)
CREATE POLICY "Lectura publica" ON public.mesures
    FOR SELECT
    USING (true);

CREATE POLICY "Lectura publica consells" ON public.consells_ia
    FOR SELECT
    USING (true);

-- Policy: nomes el service_role pot ESCRIURE (el backend te aquesta clau)
CREATE POLICY "Insert amb service_role" ON public.mesures
    FOR INSERT
    WITH CHECK (auth.role() = 'service_role' OR auth.role() = 'anon');

CREATE POLICY "Insert consells" ON public.consells_ia
    FOR INSERT
    WITH CHECK (auth.role() = 'service_role' OR auth.role() = 'anon');


-- ──────────── Vistes utils ────────────

-- Ultimes N mesures d'un node
CREATE OR REPLACE VIEW public.ultimes_mesures AS
SELECT * FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY node_id ORDER BY ts DESC) AS rn
    FROM public.mesures
) t
WHERE rn <= 100;

-- Resum diari (max, min, mitjana per dia)
CREATE OR REPLACE VIEW public.resum_diari AS
SELECT
    DATE(ts) AS dia,
    node_id,
    ROUND(AVG(temperatura_c)::numeric, 1) AS temp_mitjana,
    ROUND(MIN(temperatura_c)::numeric, 1) AS temp_min,
    ROUND(MAX(temperatura_c)::numeric, 1) AS temp_max,
    ROUND(AVG(humitat_amb_pct)::numeric, 1) AS hum_amb_mitjana,
    ROUND(AVG(humitat_sol_pct)::numeric, 0) AS sol_mitjana,
    ROUND(AVG(bateria_v)::numeric, 2) AS bateria_mitjana,
    COUNT(*) AS lectures
FROM public.mesures
GROUP BY DATE(ts), node_id
ORDER BY dia DESC;


-- ──────────── Permissos ────────────
-- Dona permis d'API anon (la web nomes llegira)
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO service_role;


-- ──────────── Dades d'exemple (comentar si no vols) ────────────
-- INSERT INTO public.mesures (temperatura_c, humitat_amb_pct, pressio_hpa, humitat_sol_pct, bateria_v)
-- VALUES (18.5, 62.3, 1013.2, 45, 3.92);
