# India Commerce and Trust Signals

Load when scoring "Commerce trust" or running `commerce`. Use with `seo-ecommerce`
for product schema and feeds.

## Payments

| Signal | Check |
|--------|-------|
| UPI | Offered at checkout (QR, UPI ID, app intent). UPI carries the large majority of Indian digital payments by volume (about 84-85% per recent reports; **verify the current figure and date before quoting**). |
| Cards and net banking | Offered, with saved-card tokenisation handled by the gateway |
| Wallets | Common ones offered where relevant |
| COD | Cash on delivery available for B2C orders where logistics allow; state any fee and limits |
| EMI / pay later | Shown on product pages above a sensible price threshold, with the real monthly figure |
| Payment trust | Gateway logos and secure checkout cues shown without clutter |

Do not claim a payment method the site does not support. Check the real checkout.

## Contact and support

- WhatsApp is a primary contact channel for many Indian users. Provide
  click-to-chat: `https://wa.me/<countrycode+number>` (digits only, e.g. `91XXXXXXXXXX`).
- Visible phone number (+91, `tel:` link) and support hours in IST.
- Real business address with city and PIN.
- Regional-language support stated if offered.

## Policies and compliance (verify with a lawyer; this is a checklist, not legal advice)

- Clear return, refund and cancellation policy, linked from product and checkout pages.
- Shipping charges, delivery time by PIN code, and a PIN-code serviceability checker.
- GST: price shown as inclusive or exclusive; GST invoice available; GSTIN shown for businesses.
- Seller and grievance-officer details displayed where Indian e-commerce rules
  require them. **Check the current consumer-protection e-commerce rules.**
- Privacy policy and consent aligned with India's Digital Personal Data
  Protection Act, 2023. **Check the current rules and timelines.**

## Trust content

- Reviews with real names or verified-purchase labels; reviews in local languages.
- Photos and videos of real products and real premises.
- Clear brand story and a named team or founder.
- Third-party proof: ratings, certifications, press, marketplace seller ratings.

## Marketplace visibility

Many Indian shoppers start on marketplaces. Check whether the brand is listed on
relevant ones (for example Amazon.in, Flipkart, Meesho, JioMart, and category
sites such as Nykaa or IndiaMART for B2B). **Marketplace shares change; verify
current relevance for the category before recommending.**

## Schema

- `Product` and `Offer` with `priceCurrency: "INR"`, availability, and shipping details.
- `MerchantReturnPolicy` and `OfferShippingDetails` where applicable, with `IN` as the destination.
- `Organization` with +91 phone, address and social links.
- Validate with `seo-schema`.

## Output

Score 0-100 with a checklist table (pass / fail / unknown) and a ranked fix list.
Mark anything that could not be verified from the public site as "unknown", not "fail".
