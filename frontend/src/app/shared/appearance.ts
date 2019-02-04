import { Time } from "@angular/common";
import { Moment } from "moment";

export interface Appearance{
    name?: string,
    date?: string,
    start_time?: string,
    end_time?: string,
    organization?: string,
    location?: string,
    parking_info?: string,
    org_type?: string,
    team_type?: string,
    performance_required?: boolean,
    special_instruction?: string,
    expenses?: string,
    outside_orgs?: boolean,
    description?: string,
    status?: string
}