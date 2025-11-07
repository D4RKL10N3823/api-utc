CREATE TABLE vacantes (
    id SERIAL PRIMARY KEY,
    nombre_empresa VARCHAR(255) NOT NULL,
    datos_vacante TEXT
);

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    carrera VARCHAR(150),
    cuatrimestre SMALLINT,
    password_hash VARCHAR(255) NOT NULL
);

CREATE EXTENSION vector;

CREATE TABLE cv_features (
  usuario_id BIGINT PRIMARY KEY REFERENCES usuarios(id) ON DELETE CASCADE,
  texto      TEXT NOT NULL,
  skills     JSONB NOT NULL DEFAULT '[]'::jsonb,
  embedding  vector(1024) NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE vacante_features (
  vacante_id BIGINT PRIMARY KEY REFERENCES vacantes(id) ON DELETE CASCADE,
  jd_text    TEXT NOT NULL,
  jd_terms   JSONB NOT NULL DEFAULT '[]'::jsonb,
  embedding  vector(1024) NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);