INSERT INTO stock (
    alert_quantity, branch_id, cost_price, created_by, created_date, desired_quantity,
    expiry_date, id, is_active, is_taxable, last_modified_by, last_modified_date,
    notification_period, price_before_tax, product_id, promotion, promotion_amt,
    promotion_percentage, promotion_price, quantity, selling_price, strength,
    tax_amount, tax_rate
)
SELECT
    s.alert_quantity, b2_new.id, s.cost_price, s.created_by, CURRENT_TIMESTAMP, s.desired_quantity,
    s.expiry_date, NULL, s.is_active, s.is_taxable, s.last_modified_by, CURRENT_TIMESTAMP,
    s.notification_period, s.price_before_tax, s.product_id, s.promotion, s.promotion_amt,
    s.promotion_percentage, s.promotion_price, s.quantity, s.selling_price, s.strength,
    s.tax_amount, s.tax_rate
FROM
    users AS u1
    INNER JOIN jungo.business AS b ON u1.id = b.owner_id
    INNER JOIN jungo.branch AS b2 ON b.id = b2.business_id
    INNER JOIN stock AS s ON s.branch_id = b2.id
    INNER JOIN users AS u2 ON u2.id > 3000
    INNER JOIN jungo.business AS b_new ON u2.id = b_new.owner_id
    INNER JOIN jungo.branch AS b2_new ON b_new.id = b2_new.business_id
WHERE
    u1.id = 1536;

# roles

INSERT INTO users_roles (user_id, role_id)
SELECT u.id, 11
FROM users u
WHERE u.id > 3000
  AND NOT EXISTS (
    SELECT 11
    FROM users_roles ur
    WHERE ur.user_id = u.id
);