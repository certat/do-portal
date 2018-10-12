with recursive iter (n, abbreviation, full_name, display_name, parent_org_id, deleted) as
    (select 1, 'Mass org abbr 1', 'Mass org full name 1', 'Mass org display name 1', __PARENT_ORG__, 0
    union
    select n+1, 'Mass org abbr ' || n+1, 'Mass org full name ' || n+1, 'Mass org display name ' || n+1, __PARENT_ORG__, 0 from iter where n < 5000)
    insert into organizations (abbreviation, full_name, display_name, parent_org_id, deleted)
    select abbreviation, full_name, display_name, parent_org_id, deleted from iter;

with recursive iter (n, organization_id, membership_role_id, email, deleted, user_id) as
    (select 1, __FIRST_ORG_ID__+1, __ROLE__, 'massorgmail' || 1 || '@example.com', 0, __USER_ACCOUNT__
    union
    select n+1, __FIRST_ORG_ID__+n+1, 1, 'massorgmail' || n+1 || '@example.com', 0, __USER_ACCOUNT__ from iter where n < 5000)
    insert into organization_memberships (organization_id, membership_role_id, email, deleted, user_id)
    select organization_id, membership_role_id, email, deleted, user_id from iter;
