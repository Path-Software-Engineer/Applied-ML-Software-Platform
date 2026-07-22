FROM node:24.15.0-alpine AS build

WORKDIR /workspace/frontend/dashboard-app

COPY frontend/dashboard-app/package.json frontend/dashboard-app/package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY frontend/dashboard-app/ ./

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN node -e "const value = process.env.VITE_API_BASE_URL || ''; if (!/^https:\/\/[^/]+$/.test(value)) { throw new Error('VITE_API_BASE_URL must be one exact HTTPS origin without a trailing slash.'); }"
RUN npm run build:minified

FROM node:24.15.0-alpine AS runtime

ENV NODE_ENV=production \
    PORT=8080 \
    STATIC_ROOT=/app/dist

WORKDIR /app

COPY deployment/docker/serve-frontend.mjs ./serve-frontend.mjs
COPY --from=build /workspace/frontend/dashboard-app/dist ./dist

RUN chown -R node:node /app
USER node

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD node -e "fetch('http://127.0.0.1:' + (process.env.PORT || '8080') + '/healthz').then(r => { if (!r.ok) process.exit(1); }).catch(() => process.exit(1))"

CMD ["node", "serve-frontend.mjs"]
