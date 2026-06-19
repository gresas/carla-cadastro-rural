# ── Build ────────────────────────────────────────────────────────────────────
FROM node:lts-alpine AS builder
WORKDIR /app/website
COPY website/package.json website/package-lock.json ./
RUN npm ci
COPY website/ .
# GitHub Pages usa baseUrl '/carla-cadastro-rural/'; k3s serve da raiz
RUN sed -i "s|baseUrl: '/carla-cadastro-rural/'|baseUrl: '/'|" docusaurus.config.ts
RUN npm run build

# ── Runtime ──────────────────────────────────────────────────────────────────
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/website/build /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
