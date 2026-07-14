/* Global type declaration for CSS Modules */
declare module "*.module.css" {
  const classes: { readonly [key: string]: string }
  export default classes
}

/* Global type declaration for image assets */
declare module "*.svg" {
  const src: string
  export default src
}
declare module "*.png" {
  const src: string
  export default src
}
declare module "*.webp" {
  const src: string
  export default src
}
