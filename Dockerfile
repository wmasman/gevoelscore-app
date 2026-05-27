# Multi-stage Dockerfile for the Next.js frontend on Fly.io.
# Uses Next's standalone output (configured in next.config.ts) for a minimal
# runtime image.

# ---- deps ------------------------------------------------------------------
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
# Tailwind v4 uses lightningcss, which ships its native binary as an
# optionalDependency (one per platform). Must NOT use --omit=optional or
# the alpine/linux-x64-musl binary is skipped and the build fails.
RUN npm ci

# ---- builder ---------------------------------------------------------------
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# ---- runner ----------------------------------------------------------------
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs

# Standalone bundle ships node_modules subset + server.js
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs
EXPOSE 3000

CMD ["node", "server.js"]
